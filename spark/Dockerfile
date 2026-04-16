FROM ubuntu:22.04

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk python3-pip curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Spark
RUN curl -L https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz | tar xz -C /opt/ && \
    mv /opt/spark-3.5.0-bin-hadoop3 /opt/spark && \
    chmod +x /opt/spark/bin/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    boto3==1.28.57 \
    pandas==2.0.3 \
    pyarrow==13.0.0 \
    numpy==1.24.3

# Add Hadoop AWS and AWS SDK JARs for S3 compatibility with MinIO
RUN cd /opt/spark/jars && \
    curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

RUN mkdir -p /opt/spark-jobs && \
    chmod 777 /opt/spark-jobs

# Set Spark home and ensure spark-submit is in PATH
ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

WORKDIR /opt/spark-jobs