class ConfigParser:
    def __init__(self, config: dict):
        self.general = GeneralConfig(config.get('general', {}))
        self.worker = WorkerConfig(config.get('worker', {}))

        metrics = config.get('metrics', {})
        self.metrics = {
            metric: MetricConfig(metrics.get(metric, {}))
            for metric in metrics.keys()
        }


class ThresholdConfig:
    def __init__(self,
                 config: dict,
                 min_default: int = None,
                 max_default: int = None):
        self.min = config.get('min', min_default)
        self.max = config.get('max', max_default)


class GeneralConfig:
    def __init__(self, config: dict):
        self.interval_seconds = float(config.get('interval_seconds', 30.0))
        self.cooldown_period_seconds = float(
            config.get('cooldown_period_seconds', 180.0))
        self.recurrence_factor = int(config.get('recurrence_factor', 5))
        self.prometheus_url = config.get('prometheus_url', None)


class WorkerConfig:
    def __init__(self, config: dict):
        self.service_name = config.get('service_name', None)
        self.network = config.get('network', None)
        self.spark_master_uri = config.get('spark_master_uri', None)
        self.thresholds = ThresholdConfig(config.get('thresholds', {}))
        self.container = ContainerConfig(config.get('container', {}))


class ContainerConfig:
    def __init__(self, config: dict):
        self.image = config.get('image', None)
        self.name_prefix = config.get('name_prefix', '')
        self.network = config.get('network', None)
        self.environment = config.get('environment', [])
        self.volumes = config.get('volumes', {})
        self.runtime = config.get('runtime', '')


class MetricConfig:
    def __init__(self, config: dict):
        self.query = config.get('query', None)
        self.target_utilization = config.get('target_utilization', None)
        self.thresholds = ThresholdConfig(config.get('thresholds'))
