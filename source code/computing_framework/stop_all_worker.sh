#!/bin/bash

docker ps | grep local/cci/distributed-computing-framework/spark-images/spark-worker:3.0.1-hadoop2.7 | awk '{print $1}' | xargs docker stop