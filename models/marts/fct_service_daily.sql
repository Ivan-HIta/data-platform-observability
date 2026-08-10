select
    cast(date_trunc('day', occurred_at) as date) as event_date,
    service,
    count(*) as event_count,
    sum(case when status = 'success' then 1 else 0 end) as success_count,
    avg(duration_ms) as avg_duration_ms
from {{ ref('stg_events') }}
group by 1, 2
