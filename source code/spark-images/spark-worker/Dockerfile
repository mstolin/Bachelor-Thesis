ARG IMAGE_TAG_PATH
ARG SPARK_VERSION
ARG HADOOP_VERSION

FROM $IMAGE_TAG_PATH/spark-base:$SPARK_VERSION-hadoop$HADOOP_VERSION

LABEL maintainer="marcel.pascal.stolin@ipa.fraunhofer.de"

# Add spark-env
COPY spark-env.sh ${SPARK_HOME}/conf/spark-env.sh

# Set port
ENV SPARK_WORKER_WEBUI_PORT 4041

EXPOSE 4041

# Start worker-node
ENTRYPOINT ./sbin/start-slave.sh ${SPARK_MASTER_URI}