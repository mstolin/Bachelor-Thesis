import math
import logging
import asyncio

from collector import Collector
from worker_scaler import WorkerScaler
from worker_scaler.docker_helper import DockerHelper
from heat_store import HeatStore


class MainLoop:
    def __init__(self, config_parser):
        self._logger = logging.getLogger(__name__)
        self._config_parser = config_parser
        self._collector = Collector(self._config_parser.general.prometheus_url)
        self._worker_scaler = WorkerScaler(
            self._config_parser.worker,
            self._config_parser.general.prometheus_url,
            self._config_parser.general.cooldown_period_seconds)
        self._heat_store = HeatStore()
        self._docker_helper = DockerHelper()

    def _calculate_number_of_worker(self, running_worker: int,
                                    utilization: float,
                                    target_utilization: float):
        return math.ceil(running_worker * (utilization / target_utilization))

    def _get_worker_number(self, response, num_running_worker: int):
        """
        Returns the number of worker needed for the metric.
        """
        if response is None:
            self._logger.warn(
                "Number of Spark worker can't be calculated. Response is empty."
            )
        else:
            metric = response.name
            utilization = response.utilization

            self._logger.info(
                f'{metric} - utilization: {utilization*100:.4f}%')

            config = self._config_parser.metrics.get(metric, None)
            if config is not None:
                # Calculate heat (analyze)
                self._heat_store.update_heat(metric, config.thresholds,
                                             utilization)
                heat = self._heat_store.get_heat(metric)
                self._logger.info(f'{metric} - Heat: {heat}')

                # Calculate number of worker if needed (Plan)
                recurrence_factor = self._config_parser.general.recurrence_factor
                if heat == recurrence_factor or heat == -recurrence_factor:
                    worker_number = self._calculate_number_of_worker(
                        num_running_worker, utilization,
                        config.target_utilization)

                    self._logger.info(
                        f'{metric} - Number of worker needed: {worker_number} (current: {num_running_worker})'
                    )

                    # reset heat
                    self._heat_store.reset_heat(metric)

                    return self._calculate_number_of_worker(
                        num_running_worker, utilization,
                        config.target_utilization)

        return 0

    async def run(self):
        num_running_worker = len(
            self._worker_scaler.get_list_of_running_worker())

        # check if the min number of worker is available
        min_worker = self._config_parser.worker.thresholds.min
        if num_running_worker < min_worker:
            self._logger.warn(
                f'Minimum number of worker ({min_worker}) is not available')
            self._docker_helper.run_container(
                min_worker, self._config_parser.worker.container)

        metrics = self._config_parser.metrics
        queries = {metric: metrics[metric].query for metric in metrics}

        responses = await self._collector.fetch_metrics(queries)

        # get needed number for each metric
        new_worker = list(
            map(
                lambda response: self._get_worker_number(
                    response, num_running_worker), responses))

        # deploy number of worker if needed (Execute phase)
        if len(new_worker) > 0:
            max_number = max(new_worker)

            if max_number > 0:
                if max_number == num_running_worker:
                    self._logger.info(
                        f'No scaling action needed. Number of needed worker ({max_number}) is equal to number of running worker ({num_running_worker}).'
                    )
                else:
                    # scale
                    self._logger.info(
                        f'New number of Spark worker needed: {max_number}')
                    await self._worker_scaler.scale(max_number)
