"""Small, dependency-free Kafka message contract for streaming ingestion.

The portfolio demo keeps the decoder pure so it can be tested without a broker.
In production, pass ``ConsumerRecord.value`` to ``decode_event`` and publish the
returned key to a partitioned topic or stream processor.
"""

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class StreamEvent:
    event_id: str
    event_type: str
    occurred_at: str
    payload: Mapping[str, Any]


def decode_event(message: bytes | str) -> StreamEvent:
    """Decode and validate the minimal event envelope from Kafka."""

    raw = message.decode("utf-8") if isinstance(message, bytes) else message
    data = json.loads(raw)
    required = {"event_id", "event_type", "occurred_at", "payload"}
    missing = required.difference(data)
    if missing:
        raise ValueError(f"missing event fields: {sorted(missing)}")
    if not isinstance(data["payload"], dict):
        raise ValueError("payload must be a JSON object")
    return StreamEvent(
        event_id=str(data["event_id"]),
        event_type=str(data["event_type"]),
        occurred_at=str(data["occurred_at"]),
        payload=data["payload"],
    )


def partition_key(event: StreamEvent) -> str:
    """Return a stable, non-sensitive key for ordering related events."""

    digest = hashlib.sha256(event.event_id.encode("utf-8")).hexdigest()
    return digest[:16]
