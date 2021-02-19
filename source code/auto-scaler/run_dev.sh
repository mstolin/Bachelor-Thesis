#!/bin/bash

PWD=$(pwd)

python3 $PWD/src/run.py --config=$PWD/tests/assets/config.yml --logging=$PWD/logging.conf
