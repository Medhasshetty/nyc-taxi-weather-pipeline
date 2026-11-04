select
    trip_id, pickup_ts, pickup_zone_id, dropoff_zone_id,
    trip_distance, fare_amount, tip_amount, total_amount,
    duration_min, weather_category
from {{ ref('int_trips_enriched') }}