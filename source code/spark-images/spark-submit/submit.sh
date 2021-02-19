#!/bin/bash

DRIVER_MEMORY=${DRIVER_MEMORY-4g}
EXECUTOR_MEMORY=${EXECUTOR_MEMORY-8g}

if [ "$CPU_ONLY" == "true" ]
  then
  echo "Submit Spark app with CPU only"

  $SPARK_HOME/bin/spark-submit \
    --master $SPARK_MASTER_URI \
    --driver-memory $DRIVER_MEMORY \
    --executor-memory $EXECUTOR_MEMORY \
    --conf spark.driver.extraClassPath=${SPARK_CUDF_JAR}:${JAR_RAPIDS}:${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar:${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar \
    --conf spark.executor.extraClassPath=${SPARK_CUDF_JAR}:${JAR_RAPIDS}:${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar:${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar \
    --jars ${SPARK_CUDF_JAR},${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar,${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar,${JAR_RAPIDS} \
    --py-files ${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar,/tank/data/users/chh-ms/spark-xgboost-examples/examples/apps/python/samples.zip \
    $@
else
  echo "Submit Spark app with GPU acceleration"

  RAPIDS_GPU_ALLOC_FRACTION=${RAPIDS_GPU_ALLOC_FRACTION-1}
  RAPIDS_INCOMPATIBLE_OPS=${RAPIDS_INCOMPATIBLE_OPS-"false"}
  RAPIDS_DEBUG=${RAPIDS_DEBUG-"NONE"}
  RAPIDS_GPU_POOL=${RAPIDS_GPU_POOL-"ARENA"}

  $SPARK_HOME/bin/spark-submit \
    --master $SPARK_MASTER_URI \
    --driver-memory $DRIVER_MEMORY \
    --executor-memory $EXECUTOR_MEMORY \
    --conf spark.plugins=com.nvidia.spark.SQLPlugin \
    --conf spark.rapids.memory.gpu.pool=$RAPIDS_GPU_POOL \
    --conf spark.rapids.memory.gpu.allocFraction=$RAPIDS_GPU_ALLOC_FRACTION \
    --conf spark.rapids.sql.incompatibleOps.enabled=$RAPIDS_INCOMPATIBLE_OPS \
    --conf spark.rapids.memory.gpu.debug=$RAPIDS_DEBUG \
    --conf spark.task.resource.gpu.amount=1 \
    --conf spark.executor.resource.gpu.amount=1 \
    --conf spark.driver.extraClassPath=${SPARK_CUDF_JAR}:${JAR_RAPIDS}:${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar:${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar \
    --conf spark.executor.extraClassPath=${SPARK_CUDF_JAR}:${JAR_RAPIDS}:${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar:${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar \
    --jars ${SPARK_CUDF_JAR},${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar,${LIBS_PATH}/xgboost4j_3.0-1.3.0-0.1.0.jar,${JAR_RAPIDS} \
    --py-files ${LIBS_PATH}/xgboost4j-spark_3.0-1.3.0-0.1.0.jar,/tank/data/users/chh-ms/spark-xgboost-examples/examples/apps/python/samples.zip \
    $@
fi