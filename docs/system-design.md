# System design interview brief

## Requirements

- Ingest batch and streaming operational events.
- Preserve event identity so retries are idempotent.
- Reject invalid records before they reach analytical marts.
- Make freshness, completeness, duplicates and latency observable.
- Scale workers independently from the dashboard.

## Proposed design

```text
producers -> Kafka / object landing -> bronze
                         |             |
                    replay/DLQ     Airflow DAG
                                       |
                               validation + dbt
                                       |
                              silver -> gold marts
                                       |
                         warehouse / semantic layer / dashboard
```

Airflow owns scheduling and retries; Kafka absorbs bursty traffic; dbt owns warehouse
transformations and tests; Kubernetes provides isolated runtime capacity; Terraform
keeps infrastructure changes reviewable. OpenTelemetry-compatible counters and logs
should be emitted at each boundary.

## Trade-offs

- Batch is simpler and cheaper for daily reporting; streaming is justified when a
  decision depends on low-latency events.
- A warehouse-first dbt layer improves discoverability; Spark is preferable when
  transformations exceed warehouse limits.
- At-least-once delivery plus deterministic keys is easier to operate than attempting
  exactly-once semantics across every external system.
