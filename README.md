# Data Platform Observability

Production-style batch data platform demo for a senior Data / ML Engineer portfolio.
It simulates incremental operational events, validates and deduplicates them, writes a
warehouse-ready dataset, and exposes data-quality and pipeline-health metrics through a
small Streamlit dashboard.

## Why this project matters

This is the evidence recruiters need beyond a notebook: idempotent ingestion, schema
validation, freshness/completeness checks, a medallion-style layout, CI tests,
containerization, observability and infrastructure-as-code references.

## Architecture

```text
synthetic source -> bronze CSV -> validated silver -> gold aggregates -> dashboard
                         |             |                 |
                         +-------- quality metrics -------+
```

The demo is intentionally cloud-neutral. The same contracts can be mapped to GCS/S3,
Spark/Databricks, BigQuery/Snowflake and Airflow/Dagster without exposing confidential
data.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.generate_data --output data/raw/events.csv --rows 5000
python -m src.pipeline --input data/raw/events.csv --output data/curated
streamlit run src/dashboard.py
pytest -q
```

## Engineering evidence

- Incremental load with deterministic event keys and idempotent reruns.
- Explicit schema, null, duplicate, freshness and referential-integrity checks.
- Bronze/silver/gold data contracts and a dbt model contract example.
- Pipeline metrics suitable for OpenTelemetry/Cloud Monitoring integration.
- Docker, GitHub Actions and Terraform reference for a cloud object store and warehouse.
- Synthetic data only; no employer data, credentials or immigration documents belong here.

## Demo narrative

“I designed a repeatable data product that can ingest operational events, stop bad data
before it reaches analytics, publish trusted aggregates and make failures visible to the
team responsible for the platform.”

