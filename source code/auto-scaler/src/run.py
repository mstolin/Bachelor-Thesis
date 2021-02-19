import argparse
import asyncio
import sys
import yaml
import os
import logging
import logging.config
from pathlib import Path

from config_parser import ConfigParser
from scheduler import Scheduler
from main_loop import MainLoop


def add_args(arg_parser):
    arg_parser.add_argument('--config',
                            type=Path,
                            help='Auto-scaler config file path',
                            required=True)
    arg_parser.add_argument('--logging',
                            type=Path,
                            help='Logging config file path')


def set_logging_config(config_file_path: str):
    try:
        logging.config.fileConfig(config_file_path)
    except:
        logging.warning(
            f'Could not load logging configuration file at {args.logging}')


def read_config(config_file_path: str):
    with open(config_file_path) as config_file:
        config = yaml.full_load(config_file)

        if config is None:
            raise Exception()

        return config


def init_config_parser(config_file_path: str):
    try:
        config = read_config(config_file_path)
        return ConfigParser(config)
    except:
        logging.critical(
            f'Could not read the configuration at {config_file_path}')
        sys.exit()


def run_loop(config_parser: ConfigParser):
    main_loop = MainLoop(config_parser)
    scheduler = Scheduler(config_parser.general.interval_seconds)
    scheduler.run(main_loop)


if __name__ == "__main__":
    # Init arg-parser
    arg_parser = argparse.ArgumentParser(
        description='The Apache Spark Worker Auto-Scaler process.')
    add_args(arg_parser)
    args = arg_parser.parse_args()

    # Set logging config
    if args.logging is not None:
        set_logging_config(args.logging)

    # Init config parser
    config_parser = init_config_parser(args.config)
    run_loop(config_parser)

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        print('\nAuto-scaler has exited.')
