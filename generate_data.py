"""Generate safe synthetic operational events for the demo."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate_events(rows: int = 5_000, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2026-01-01", periods=rows, freq="15min")
    regions = rng.choice(["AB", "ON", "BC", "NS"], size=rows, p=[0.25, 0.45, 0.2, 0.1])
    status = rng.choice(["completed", "delayed", "cancelled"], size=rows, p=[0.86, 0.1, 0.04])
    frame = pd.DataFrame(
        {
            "event_id": [f"evt-{i:07d}" for i in range(rows)],
            "event_ts": timestamps,
            "region": regions,
            "service": rng.choice(["delivery", "pickup", "transfer"], size=rows),
            "status": status,
            "duration_minutes": np.maximum(1, rng.normal(42, 13, rows).round(1)),
            "revenue": np.maximum(0, rng.normal(125, 35, rows).round(2)),
        }
    )
    # A small controlled defect rate makes the quality dashboard meaningful.
    frame.loc[frame.index[::173], "region"] = None
    frame.loc[frame.index[::241], "event_id"] = frame.loc[frame.index[0], "event_id"]
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/events.csv")
    parser.add_argument("--rows", type=int, default=5_000)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_events(args.rows).to_csv(output, index=False)
    print(f"wrote {args.rows:,} synthetic events to {output}")


if __name__ == "__main__":
    main()

