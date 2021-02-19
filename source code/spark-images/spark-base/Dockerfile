FROM nvidia/cuda:10.2-devel-ubuntu18.04

LABEL maintainer="marcel.pascal.stolin@ipa.fraunhofer.de"

ARG SPARK_VERSION
ARG HADOOP_VERSION

# Install all important packages
RUN apt-get update -y && \
    apt-get install -y openjdk-8-jre-headless python3-distutils python3-apt software-properties-common procps curl
# Set Java Home
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Install Python 3.8
RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y python3.8 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# Install pip
RUN mkdir /opt/pip/ && \
    curl https://bootstrap.pypa.io/get-pip.py -o /opt/pip/get-pip.py && \
    python3 /opt/pip/get-pip.py && \
    rm -rf /opt/pip/

# Update pip and install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install pyspark numpy pandas

# Install Apache Spark
RUN mkdir /usr/bin/spark/ && \
    curl https://ftp-stud.hs-esslingen.de/pub/Mirrors/ftp.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/* /usr/bin/spark/ && \
    rm -rf spark.tgz && \
    rm -rf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/
ENV SPARK_HOME /usr/bin/spark

# Add GPU discovery script
RUN mkdir /opt/resourceDiscovery/
COPY getGpusResources.sh /opt/resourceDiscovery/getGpusResources.sh
ENV GPU_DISCOVERY_SCRIPT=/opt/resourceDiscovery/getGpusResources.sh

# Install cuDF, RAPIDS and XGBoost
ENV LIBS_PATH=${SPARK_HOME}/jars
RUN curl -o ${LIBS_PATH}/cudf-0.17-cuda10-2.jar https://repo1.maven.org/maven2/ai/rapids/cudf/0.17/cudf-0.17-cuda10-2.jar
RUN curl -o ${LIBS_PATH}/rapids-4-spark_2.12-0.3.0.jar https://repo1.maven.org/maven2/com/nvidia/rapids-4-spark_2.12/0.3.0/rapids-4-spark_2.12-0.3.0.jar
RUN curl -o ${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar https://repo1.maven.org/maven2/com/nvidia/xgboost4j-spark_3.0/1.3.0-0.1.0/xgboost4j-spark_3.0-1.3.0-0.1.0.jar
RUN curl -o ${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar https://repo1.maven.org/maven2/com/nvidia/xgboost4j_3.0/1.3.0-0.1.0/xgboost4j_3.0-1.3.0-0.1.0.jar
ENV SPARK_CUDF_JAR=${LIBS_PATH}/cudf-0.17-cuda10-2.jar
ENV RAPIDS_JAR=${LIBS_PATH}/rapids-4-spark_2.12-0.3.0.jar
ENV SPARK_JARS=${SPARK_CUDF_JAR}:${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar:${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar

# Set all environment variables
ENV SPARK_NO_DAEMONIZE true
ENV PYSPARK_DRIVER_PYTHON python3
ENV PYSPARK_PYTHON python3
ENV PATH /usr/bin/spark/bin:/usr/bin/spark/sbin:$PATH
ENV PYTHONPATH ${PYTHONPATH}:${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar

WORKDIR ${SPARK_HOME}