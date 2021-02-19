ARG IMAGE_TAG_PATH
ARG SPARK_VERSION
ARG HADOOP_VERSION

FROM $IMAGE_TAG_PATH/spark-base:$SPARK_VERSION-hadoop$HADOOP_VERSION

LABEL maintainer="marcel.pascal.stolin@ipa.fraunhofer.de"

# Set ports
ENV SPARK_MASTER_PORT 7077
ENV SPARK_MASTER_WEBUI_PORT 4040

EXPOSE 4040 7077

# Start master-node in standalone mode
ENTRYPOINT [ "sbin/start-master.sh" ]