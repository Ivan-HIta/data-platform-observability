select
    cast(event_id as varchar) as event_id,
    cast(event_type as varchar) as event_type,
    cast(service as varchar) as service,
    cast(status as varchar) as status,
    cast(occurred_at as timestamp) as occurred_at,
    cast(duration_ms as integer) as duration_ms
from {{ source('raw', 'events') }}
where event_id is not null
