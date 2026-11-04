select
    date_trunc('hour', pickup_ts)  as hour_ts,
    pickup_borough,
    weather_category,
    count(*)                       as trips,
    sum(total_amount)              as revenue,
    avg(trip_distance)             as avg_distance,
    avg(tip_amount / nullif(fare_amount, 0)) as avg_tip_pct
from {{ ref('int_trips_enriched') }}
group by 1, 2, 3