# Flight Analytics Data Engineering Project

## Overview

This project implements an end-to-end data engineering pipeline for aviation analytics using the OPDI Flight List dataset.

The pipeline ingests raw flight data, processes it through a multi-layer architecture (bronze → silver → gold), and delivers analytics-ready datasets in a cloud data warehouse.

The project follows the Data Engineering Zoomcamp evaluation criteria, focusing on reproducibility, orchestration, data modeling, and infrastructure-as-code.

---

## Problem Statement

Air traffic data is complex and high-volume. This project aims to:

* Build a scalable pipeline for ingesting and processing flight data
* Enable analysis of airline performance, delays, and traffic patterns
* Provide a structured data model for analytics and reporting

---

## Dataset

Source:
https://www.opdi.aero/flight-list-data

The dataset contains:

* Flight timestamps
* Departure and arrival airports
* Airline information
* Flight durations and delays

---

## Architecture

```
          +----------------------+
          | OPDI Flight Dataset  |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |  Data Ingestion      |
          |  (Python / Spark)    |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |  Data Lake           |
          |  (S3 / MinIO)        |
          |  Bronze Layer        |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |  Processing Layer    |
          |  (Spark)             |
          |  Silver Layer        |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |  Data Warehouse      |
          |  (Snowflake)         |
          |  Gold Layer          |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |  Analytics / BI      |
          +----------------------+

Orchestration: Airflow  
Infrastructure: Terraform
```

---

## Tech Stack

* **Terraform** – Infrastructure as Code
* **Snowflake** – Data Warehouse
* **Apache Spark** – Data Processing
* **dbt** – Data Modeling
* **Apache Airflow** – Workflow Orchestration
* **MinIO / S3** – Data Lake Storage
* **Docker Compose** – Local environment

---

## Data Pipeline

### 1. Ingestion

* Download raw data from OPDI
* Store in data lake (bronze layer)

### 2. Transformation (Spark)

* Clean and normalize data
* Handle nulls and duplicates
* Convert to Parquet (silver layer)

### 3. Loading

* Load cleaned data into Snowflake

### 4. Modeling (dbt)

* Build staging and mart models
* Apply tests (NOT NULL, UNIQUE)

### 5. Orchestration (Airflow)

* Schedule and manage pipeline execution

---

## Data Model

### Bronze Layer

* Raw, unprocessed data
* Stored in original format (CSV/JSON)

### Silver Layer

* Cleaned and structured data
* Stored in Parquet format

### Gold Layer

#### Fact Table

* `fact_flights`

  * flight_id
  * departure_airport
  * arrival_airport
  * delay_minutes
  * duration
  * airline_id
  * date_key

#### Dimension Tables

* `dim_airport`
* `dim_airline`
* `dim_date`

---

## Use Cases

* Identify most delayed routes
* Analyze airline performance
* Detect busiest airports
* Explore seasonal trends in air traffic

---

## Orchestration (Airflow DAG)

Pipeline steps:

1. `ingest_opdi_data`
2. `upload_to_data_lake`
3. `spark_transform`
4. `load_to_snowflake`
5. `dbt_run`
6. `dbt_test`

---

## Infrastructure (Terraform)

Provisioned resources:

* Snowflake:

  * Warehouse
  * Database
  * Schema
  * Roles
* S3 / MinIO bucket

---

## Project Structure

```
flight-analytics-project/
│
├── terraform/
├── airflow/
│   └── dags/
├── spark/
│   └── jobs/
├── dbt/
│   └── models/
├── data/
├── docker-compose.yml
└── README.md
```

---

## How to Run

### 1. Clone repository

```
git clone <repo-url>
cd flight-analytics-project
```

### 2. Start services

```
docker-compose up -d
```

### 3. Initialize infrastructure

```
cd terraform
terraform init
terraform apply
```

### 4. Run pipeline

* Trigger DAG in Airflow UI

---

## Evaluation Criteria Mapping

| Criteria            | Implementation     |
| ------------------- | ------------------ |
| Problem description | Aviation analytics |
| Cloud               | Snowflake + S3     |
| Data ingestion      | Python / Spark     |
| Data warehouse      | Snowflake          |
| Transformations     | Spark + dbt        |
| Orchestration       | Airflow            |
| Reproducibility     | Terraform + Docker |
| Dashboard           | Optional           |

---

## Future Improvements

* Incremental data loading
* Data quality checks (Great Expectations)
* CI/CD pipeline (GitHub Actions)
* Dashboard (Metabase / Superset)
* Performance optimization

---

## Author

Jurii

---
