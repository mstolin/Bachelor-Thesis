#!/bin/bash

docker swarm init && \
docker stack deploy -c $(pwd)/docker-compose_dev.yml computing
