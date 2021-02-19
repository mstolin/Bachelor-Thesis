import aiohttp
import asyncio


class Collector:
    def __init__(self, url: str):
        self._url = url

    def _parse_response(self, metric_name: str, response: dict):
        data = response.get('data', {})
        result = data.get('result', [])

        if len(result) == 0:
            return None

        # second entry is the metric value, first one the timestamp
        utilization = sum(
            list(map(lambda metric: float(metric.get('value', [])[-1]),
                     result)))

        return MetricResponse(metric_name, utilization)

    async def fetch_query(self, metric: str, query: str):
        url = f'{self._url}/api/v1/query?query={query}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    json = await response.json()
                    if json.get('status', '') == 'success':
                        parsed_response = self._parse_response(metric, json)
                        return parsed_response
                    else:
                        # log
                        return None
            except:
                return None

    async def fetch_metrics(self, metrics: dict):
        #completed, pending = await asyncio.wait([
        #    self.fetch_query(metric, metrics[metric])
        #    for metric in metrics.keys()
        #])

        #for t in pending:
        #    t.cancel()

        import random

        return [
            MetricResponse(metric,
                           0)  #MetricResponse(metric, random.uniform(0.6, 1))
            for metric in metrics.keys()
        ]


class MetricResponse:
    def __init__(self, name: str, utilization: float):
        self.name = name
        self.utilization = utilization