select
    hour_ts,
    temperature_2m   as temperature_c,
    precipitation    as precipitation_mm,
    wind_speed_10m   as wind_kmh,
    case
        when precipitation > 0.5 then 'rain'
        when temperature_2m < 0  then 'freezing'
        else 'clear'
    end as weather_category
from {{ source('raw', 'weather') }}