import os
import yaml
import uuid
import random
import logging
import aiohttp
import asyncio
from datetime import datetime

from collector import Collector
from .docker_helper import DockerHelper


class WorkerScaler():
    def __init__(self, config, prometheus_url: str, cooldown_period: float):
        self._config = config
        self._prometheus_url = prometheus_url
        self._logger = logging.getLogger(__name__)
        self._collector = Collector(prometheus_url)
        self._docker_helper = DockerHelper()
        self._cooldown_period = cooldown_period
        self._cooldown_timestamp = 0

    async def _get_number_of_running_apps(self):
        response = await self._collector.fetch_query(
            'apps', 'metrics_master_apps_Number')

        if response is None:
            return None

        running_apps = int(response.utilization)
        return running_apps

    def _set_cooldown(self):
        if self._cooldown_timestamp is not None:
            self._cooldown_timestamp = datetime.now().timestamp(
            ) + self._cooldown_period
            self._logger.info(f'Set cooldown to {self._get_cooldown_time()}')

    def _get_cooldown_time(self):
        return datetime.fromtimestamp(self._cooldown_timestamp)

    def _run_container(self):
        pass

    def get_list_of_running_worker(self):
        return self._docker_helper.get_list_of_containers(
            self._config.container.image)

    async def scale(self, replicas: int):
        now = datetime.now().timestamp()
        if now < self._cooldown_timestamp:
            # cooldown is still activated
            self._logger.info(
                f'Cooldown is activated until {self._get_cooldown_time()}')
        else:
            running_worker = self.get_list_of_running_worker()
            num_running_worker = len(running_worker)
            upper_threshold = self._config.thresholds.max
            lower_threshold = self._config.thresholds.min
            service_name = self._config.service_name

            if replicas > upper_threshold:
                # upper threhold violation
                self._logger.warn(
                    f'Upper threshold violation. Needed worker: {replicas}, upper threshold: {upper_threshold}.'
                )
                replicas = upper_threshold
            elif replicas < lower_threshold:
                # lower threshold violation
                self._logger.warn(
                    f'Lower threshold violation. Needed worker: {replicas}, lower threshold: {lower_threshold}.'
                )
                replicas = lower_threshold

            # now scale
            self._logger.debug(
                f'Going to scale service {service_name} to {replicas} replicas'
            )

            if num_running_worker > replicas:
                # scale-in
                self._logger.info('Scale-in action is needed.')
                num_running_apps = await self._get_number_of_running_apps()
                if num_running_apps > 0:
                    # do not scale if any applications are running
                    self._logger.warn(
                        f'{num_running_apps} Spark apps are running. Worker will not be remove for now.'
                    )
                    return
                else:
                    # no apps running
                    self._logger.debug('No applications are running.')
                    container_to_remove = num_running_worker - replicas
                    self._docker_helper.remove_container(
                        container_to_remove, self._config.container)
            else:
                # scale-out
                success = self._docker_helper.run_container(
                    replicas, self._config.container)

                if success:
                    self._logger.info(
                        f'Successfully scaled service {service_name} to {replicas} replicas.'
                    )

                    self._set_cooldown()
                else:
                    self._logger.error(
                        f'Failed to scale service {service_name} to {replicas} replicas.'
                    )
