select
    "LocationID"  as zone_id,
    "Borough"     as borough,
    "Zone"        as zone_name
from {{ source('raw', 'zones') }}