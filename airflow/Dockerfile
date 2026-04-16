FROM apache/airflow:2.9.1

USER root


ENV HADOOP_AWS_VERSION=3.3.4
ENV AWS_SDK_VERSION=1.12.262

# Java for Spark
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Spark client
ENV SPARK_VERSION=3.5.0


RUN curl -L -o /opt/airflow/hadoop-aws-${HADOOP_AWS_VERSION}.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    curl -L -o /opt/airflow/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar

ENV SPARK_CLASSPATH="/opt/airflow/hadoop-aws-${HADOOP_AWS_VERSION}.jar:/opt/airflow/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar"

ENV SPARK_HOME=/opt/spark-3.5.0-bin-hadoop3
ENV PATH=$SPARK_HOME/bin:$PATH

USER airflow