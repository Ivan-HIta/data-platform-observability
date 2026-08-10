import pandas as pd

from src.pipeline import transform, validate_schema


def test_schema_contract_reports_missing_fields():
    assert validate_schema(pd.DataFrame({"event_id": ["a"]}))


def test_transform_deduplicates_and_removes_invalid_rows():
    frame = pd.DataFrame(
        {
            "event_id": ["a", "a", "b"],
            "event_ts": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "region": ["AB", "AB", None],
            "service": ["delivery", "delivery", "pickup"],
            "status": ["completed"] * 3,
            "duration_minutes": [10, 20, 30],
            "revenue": [1, 2, 3],
        }
    )
    result, quality = transform(frame)
    assert len(result) == 1
    assert quality["duplicate_event_ids"] == 1

