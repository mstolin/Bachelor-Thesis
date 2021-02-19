import yaml
from os import path

from src.config_parser import ConfigParser


def test_config_parser_is_importable():
    assert ConfigParser is not None


def _getfile_path(filename):
    return path.join(path.dirname(path.abspath(__file__)),
                     f'assets/{filename}')


#
# Full config
#
with open(_getfile_path('config.yml')) as config_file:
    config = yaml.full_load(config_file)
    config_parser_full = ConfigParser(config)


def test_config_parser_full_has_been_initialized():
    assert config_parser_full is not None


def test_config_parser_full_general_config():
    general = config_parser_full.general

    assert general.interval_seconds == 5
    assert general.cooldown_period_seconds == 180
    assert general.recurrence_factor == 3
    assert general.prometheus_url == "http://localhost:9090"


def test_config_parser_full_metrics_config():
    metrics = config_parser_full.metrics

    assert len(list(metrics.keys())) == 2

    cpu = metrics['cpu']
    cpu_thresholds = cpu.thresholds
    assert cpu.query == 'sum(rate(container_cpu_user_seconds_total{image="local/cci/distributed-computing-framework/spark-images/spark-worker:3.0.1-hadoop2.7"}[30s]))'
    assert cpu.target_utilization == 0.5
    assert cpu_thresholds.min == 0.2
    assert cpu_thresholds.max == 0.6

    gpu = metrics['gpu']
    gpu_thresholds = gpu.thresholds
    assert gpu.query == 'sum(rate(container_cpu_user_seconds_total{image="local/cci/distributed-computing-framework/spark-images/spark-worker:3.0.1-hadoop2.7"}[30s]))'
    assert gpu.target_utilization == 0.3
    assert gpu_thresholds.min == 0.2
    assert gpu_thresholds.max == 0.6


def test_config_parser_full_worker_config():
    worker = config_parser_full.worker
    worker_thresholds = worker.thresholds

    assert worker.service_name == 'computing_spark-worker'
    assert worker_thresholds.min == 1
    assert worker_thresholds.max == 30


#
# Empty config
#
config_parser_empty = ConfigParser({})


def test_config_parser_empty_has_been_initialized():
    assert config_parser_empty is not None


def test_config_parser_empty_general_config():
    general = config_parser_empty.general

    assert general.interval_seconds == 30
    assert general.cooldown_period_seconds == 180
    assert general.recurrence_factor == 5
    assert general.prometheus_url is None


def test_config_parser_empty_metrics_config():
    metrics = config_parser_empty.metrics.keys()

    assert len(metrics) == 0


def test_config_parser_empty_worker_config():
    worker = config_parser_empty.worker
    worker_thresholds = worker.thresholds

    assert worker.service_name is None
    assert worker_thresholds.min is None
    assert worker_thresholds.max is None
