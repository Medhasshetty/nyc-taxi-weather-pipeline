select
    row_number() over () as trip_id,
    "VendorID"                    as vendor_id,
    tpep_pickup_datetime          as pickup_ts,
    tpep_dropoff_datetime         as dropoff_ts,
    "PULocationID"                as pickup_zone_id,
    "DOLocationID"                as dropoff_zone_id,
    passenger_count,
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount,
    extract(epoch from (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60.0 as duration_min
from {{ source('raw', 'taxi_trips') }}
where fare_amount > 0
  and trip_distance > 0
  and tpep_dropoff_datetime > tpep_pickup_datetime
  and tpep_pickup_datetime >= '2024-01-01'
  and tpep_pickup_datetime <  '2024-02-01'