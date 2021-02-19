#!/bin/bash

if [ $# -ge 2 ]
  then
    SPARK_VERSION=$1
    HADOOP_VERSION=$2

    PWD=$(pwd)

    IMAGE_TAG_PATH="local"

    echo
    echo "# Image tag-path: ${IMAGE_TAG_PATH}"
    echo

    echo "# STEP(1/4) - Building spark-base"
    docker build \
      -t $IMAGE_TAG_PATH/spark-base:$SPARK_VERSION-hadoop$HADOOP_VERSION \
      --build-arg SPARK_VERSION=$SPARK_VERSION \
      --build-arg HADOOP_VERSION=$HADOOP_VERSION \
      $PWD/spark-base/

    echo "# STEP(2/4) - Building spark-master"
    docker build \
      -t $IMAGE_TAG_PATH/spark-master:$SPARK_VERSION-hadoop$HADOOP_VERSION \
      --build-arg IMAGE_TAG_PATH=$IMAGE_TAG_PATH \
      --build-arg SPARK_VERSION=$SPARK_VERSION \
      --build-arg HADOOP_VERSION=$HADOOP_VERSION \
      $PWD/spark-master/

    echo "# STEP(3/4) - Building spark-worker"
    docker build \
      -t $IMAGE_TAG_PATH/spark-worker:$SPARK_VERSION-hadoop$HADOOP_VERSION \
      --build-arg IMAGE_TAG_PATH=$IMAGE_TAG_PATH \
      --build-arg SPARK_VERSION=$SPARK_VERSION \
      --build-arg HADOOP_VERSION=$HADOOP_VERSION \
      $PWD/spark-worker/

    echo "# STEP(4/4) - Building spark-submit"
    docker build \
      -t $IMAGE_TAG_PATH/spark-submit:$SPARK_VERSION-hadoop$HADOOP_VERSION \
      --build-arg IMAGE_TAG_PATH=$IMAGE_TAG_PATH \
      --build-arg SPARK_VERSION=$SPARK_VERSION \
      --build-arg HADOOP_VERSION=$HADOOP_VERSION \
      $PWD/spark-submit/
  else
    echo "No arguments supplied\n"
    echo "Use the script as follows:"
    echo "build-images.sh <SPARK_VERSION> <HADOOP_VERSION>"
    exit 1
fi