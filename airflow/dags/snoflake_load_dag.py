from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import boto3
import os

from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

BUCKET = "flight-data"

with DAG(
    dag_id="silver_minio_to_snowflake",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    #--------------------------
    # Get current role
    #--------------------------
    @task
    def debug_context():
        hook = SnowflakeHook()
        print(hook.get_first("""
            SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_USER();
        """))

    # -------------------------
    # Setup Snowflake objects
    # -------------------------
    @task
    def setup_snowflake():
        hook = SnowflakeHook()

        hook.run("USE ROLE ACCOUNTADMIN;")
        hook.run("USE WAREHOUSE FLIGHT_WH;")
        hook.run("USE DATABASE FLIGHT_ANALYTICS;")
        hook.run("USE SCHEMA SILVER;")

        # target table
        hook.run("""
            CREATE TABLE IF NOT EXISTS flights (
                first_seen TIMESTAMP,
                icao24 VARCHAR,
                ADEP VARCHAR,
                ADES VARCHAR,
                year INT,
                month INT,
                day INT
            );
        """)

        # staging table (IMPORTANT)
        hook.run("""
            CREATE TABLE IF NOT EXISTS flights_stage (
                first_seen TIMESTAMP,
                icao24 VARCHAR,
                ADEP VARCHAR,
                ADES VARCHAR,
                year INT,
                month INT,
                day INT
            );
        """)

        # file stage
        hook.run("""
            CREATE STAGE IF NOT EXISTS flights_stage_files;
        """)

    # -------------------------
    # Get files from MinIO
    # -------------------------
    @task
    def get_partition_files(ds=None):
        year, month, day = ds.split("-")
        prefix = f"silver/flights/"

        s3 = boto3.client(
            "s3",
            endpoint_url="http://minio:9000",
            aws_access_key_id="minio",
            aws_secret_access_key="minio123",
        )

        files = []
        response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)

        for obj in response.get("Contents", []):
            key = obj["Key"]

            if key.endswith(".parquet"):
                filename = os.path.basename(key)
                local_path = f"/tmp/{filename}"

                s3.download_file(BUCKET, key, local_path)
                files.append(local_path)

        if not files:
            raise ValueError(f"No files found for partition {ds}")

        return files

    # -------------------------
    # Load into staging table
    # -------------------------
    @task
    def load_to_stage(files):
        hook = SnowflakeHook()

        hook.run("USE ROLE ACCOUNTADMIN;")
        hook.run("USE WAREHOUSE FLIGHT_WH;")
        hook.run("USE DATABASE FLIGHT_ANALYTICS;")
        hook.run("USE SCHEMA SILVER;")

        # clean stage storage
        hook.run("REMOVE @flights_stage_files;")

        # clean staging table (IMPORTANT for idempotency)
        hook.run("TRUNCATE TABLE flights_stage;")

        # upload files
        for f in files:
            hook.run(f"PUT file://{f} @flights_stage_files AUTO_COMPRESS=TRUE;")

        # load into staging TABLE
        hook.run("""
            COPY INTO flights_stage
            FROM @flights_stage_files
            FILE_FORMAT=(TYPE=PARQUET)
            MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
        """)

    # -------------------------
    # Merge into target table
    # -------------------------
    @task
    def merge(ds=None):
        year, month, day = ds.split("-")
        hook = SnowflakeHook()

        hook.run("USE ROLE ACCOUNTADMIN;")
        hook.run("USE WAREHOUSE FLIGHT_WH;")
        hook.run("USE DATABASE FLIGHT_ANALYTICS;")
        hook.run("USE SCHEMA SILVER;")

        hook.run(f"""
            MERGE INTO flights t
            USING (
                SELECT *
                FROM flights_stage
                WHERE year = {year}
                  AND month = {month}
                  AND day = {day}
            ) s
            ON t.icao24 = s.icao24
               AND t.first_seen = s.first_seen
            WHEN NOT MATCHED THEN
                INSERT (
                    first_seen, icao24, ADEP, ADES, year, month, day
                )
                VALUES (
                    s.first_seen,
                    s.icao24,
                    s.ADEP,
                    s.ADES,
                    s.year,
                    s.month,
                    s.day
                );
        """)

    # -------------------------
    # DAG dependencies
    # -------------------------
    debug = debug_context()
    setup = setup_snowflake()
    files = get_partition_files()
    load = load_to_stage(files)
    merge_task = merge()

    debug >> setup >> files >> load >> merge_task