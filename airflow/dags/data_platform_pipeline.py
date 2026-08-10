"""Reference Airflow DAG for the local data-platform demo.

The commands deliberately call the same deterministic modules used locally. In a
managed environment the BashOperators can be replaced by containerized tasks or
Cloud Composer operators without changing the data contracts.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="data_platform_observability",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "owner": "data-platform",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["batch", "data-quality", "portfolio"],
) as dag:
    generate = BashOperator(
        task_id="generate_synthetic_events",
        bash_command=(
            "python -m src.generate_data --output data/raw/events.csv --rows 5000"
        ),
    )

    curate = BashOperator(
        task_id="validate_and_publish_curated_data",
        bash_command=(
            "python -m src.pipeline --input data/raw/events.csv "
            "--output data/curated"
        ),
    )

    generate >> curate
