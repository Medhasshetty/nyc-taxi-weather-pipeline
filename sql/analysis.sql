-- 1. Trips by hour of day
select extract(hour from pickup_ts) as hour, count(*) as trips
from analytics.fct_trips group by 1 order by 1;

-- 2. Average trips per hour: rain vs clear vs freezing
select weather_category, round(avg(trips), 0) as avg_trips_per_hour
from (
    select hour_ts, weather_category, sum(trips) as trips
    from analytics.agg_hourly_demand
    group by 1, 2
) h
group by 1 order by 2 desc;

-- 3. Top 10 pickup zones
select z.zone_name, z.borough, count(*) as trips
from analytics.fct_trips t
join analytics.dim_zone z on t.pickup_zone_id = z.zone_id
group by 1, 2 order by 3 desc limit 10;

-- 4. Revenue by borough
select z.borough, round(sum(t.total_amount)::numeric, 0) as revenue
from analytics.fct_trips t
join analytics.dim_zone z on t.pickup_zone_id = z.zone_id
group by 1 order by 2 desc;

-- 5. Average tip % by weather
select weather_category,
       round((avg(tip_amount / nullif(fare_amount, 0)) * 100)::numeric, 2) as avg_tip_pct
from analytics.fct_trips group by 1 order by 2 desc;

-- 6. Busiest day of week (0 = Sunday)
select extract(dow from pickup_ts) as day_of_week, count(*) as trips
from analytics.fct_trips group by 1 order by 2 desc;

-- 7. Average trip duration by hour (rush hour effect)
select extract(hour from pickup_ts) as hour,
       round(avg(duration_min)::numeric, 1) as avg_minutes
from analytics.fct_trips group by 1 order by 1;

-- 8. Rank zones by revenue (window function)
select zone_name, revenue,
       rank() over (order by revenue desc) as revenue_rank
from (
    select z.zone_name, round(sum(t.total_amount)::numeric, 0) as revenue
    from analytics.fct_trips t
    join analytics.dim_zone z on t.pickup_zone_id = z.zone_id
    group by 1
) r
order by revenue_rank limit 10;