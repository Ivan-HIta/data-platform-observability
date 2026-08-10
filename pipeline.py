"""Small, testable batch pipeline with data contracts and observability metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "event_id",
    "event_ts",
    "region",
    "service",
    "status",
    "duration_minutes",
    "revenue",
}


def validate_schema(frame: pd.DataFrame) -> list[str]:
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    return [f"missing columns: {', '.join(missing)}"] if missing else []


def transform(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    errors = validate_schema(frame)
    if errors:
        raise ValueError("; ".join(errors))
    work = frame.copy()
    work["event_ts"] = pd.to_datetime(work["event_ts"], utc=True, errors="coerce")
    work["duration_minutes"] = pd.to_numeric(work["duration_minutes"], errors="coerce")
    work["revenue"] = pd.to_numeric(work["revenue"], errors="coerce")
    before = len(work)
    work = work.dropna(subset=["event_id", "event_ts", "region", "service"])
    work = work.drop_duplicates(subset=["event_id"], keep="last")
    work = work[(work["duration_minutes"] >= 0) & (work["revenue"] >= 0)]
    work["event_date"] = work["event_ts"].dt.date.astype(str)
    quality = {
        "input_rows": int(before),
        "output_rows": int(len(work)),
        "dropped_rows": int(before - len(work)),
        "duplicate_event_ids": int(before - frame["event_id"].nunique(dropna=True)),
        "null_rate": round(float(frame.isna().mean().mean()), 6),
        "freshness_max_event": work["event_ts"].max().isoformat() if not work.empty else None,
    }
    return work, quality


def run(input_path: str | Path, output_dir: str | Path) -> dict:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(input_path)
    silver, quality = transform(raw)
    silver.to_parquet(output / "silver_events.parquet", index=False)
    gold = (
        silver.groupby(["event_date", "region", "service"], as_index=False)
        .agg(events=("event_id", "count"), revenue=("revenue", "sum"), avg_duration=("duration_minutes", "mean"))
    )
    gold.to_csv(output / "gold_service_daily.csv", index=False)
    (output / "quality_metrics.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    return quality


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/curated")
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), indent=2))


if __name__ == "__main__":
    main()

