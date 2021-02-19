#!/bin/bash

if [ $# -ge 1 ]
  then
    VERSION=$1

    PWD=$(pwd)

    IMAGE_TAG_PATH="local"

    docker build \
      -t $IMAGE_TAG_PATH/auto-scaler:$VERSION \
      $PWD

    docker build \
      -t $IMAGE_TAG_PATH/auto-scaler:latest \
      $PWD
  else
    echo "No arguments supplied\n"
      echo "Use the script as follows:"
      echo "build-image.sh <VERSION>"
      exit 1
fi
