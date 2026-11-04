select
    t.*,
    z.borough      as pickup_borough,
    z.zone_name    as pickup_zone,
    w.temperature_c,
    w.precipitation_mm,
    w.weather_category
from {{ ref('stg_trips') }} t
left join {{ ref('stg_zones') }} z on t.pickup_zone_id = z.zone_id
left join {{ ref('stg_weather') }} w on date_trunc('hour', t.pickup_ts) = w.hour_ts