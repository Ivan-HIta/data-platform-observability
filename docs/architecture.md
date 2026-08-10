# Architecture and productionization path

## Current demo

The local version uses CSV and Parquet so it runs without cloud credentials. The
contracts are isolated in `src/pipeline.py`, making the storage layer replaceable.

## Production mapping

| Demo component | Cloud-ready implementation |
| --- | --- |
| Raw landing | GCS or S3 partitioned by ingestion date |
| Transformations | Spark/PySpark or Databricks job |
| Warehouse | BigQuery or Snowflake gold tables |
| Orchestration | Airflow, Cloud Composer or Dagster |
| Data quality | Great Expectations, dbt tests and contract checks |
| Observability | OpenTelemetry, Cloud Monitoring and alerting |
| Access | IAM service accounts, secret manager and least privilege |

The key design decision is that a batch rerun is safe: event keys are deterministic,
deduplication is explicit and outputs are derived from validated inputs.

