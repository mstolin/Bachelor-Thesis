ARG IMAGE_TAG_PATH
ARG SPARK_VERSION
ARG HADOOP_VERSION

FROM $IMAGE_TAG_PATH/spark-base:$SPARK_VERSION-hadoop$HADOOP_VERSION

LABEL maintainer="marcel.pascal.stolin@ipa.fraunhofer.de"

# Install python dependencies and create workdir
RUN mkdir /usr/bin/submit/ && \
    mkdir /opt/spark-apps

COPY submit.sh /usr/bin/submit/

# Set the submit script as entrypoint
ENTRYPOINT [ "/usr/bin/submit/submit.sh" ]