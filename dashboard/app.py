import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

st.title("NYC Taxi Demand vs Weather (Jan 2024)")


@st.cache_data
def q(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, engine)


hourly = q("""
    select extract(hour from hour_ts)::int as hour, weather_category,
           avg(trips) as avg_trips
    from (
        select hour_ts, weather_category, sum(trips) as trips
        from analytics.agg_hourly_demand
        group by 1, 2
    ) h
    group by 1, 2 order by 1
""")
st.subheader("Average trips by hour of day and weather")
st.line_chart(hourly.pivot(index="hour", columns="weather_category", values="avg_trips"))

zones = q("""
    select pickup_borough, sum(revenue) as revenue
    from analytics.agg_hourly_demand
    where pickup_borough is not null
    group by 1 order by 2 desc
""")
st.subheader("Revenue by borough")
st.bar_chart(zones.set_index("pickup_borough"))

tip = q("""
    select weather_category, avg(avg_tip_pct) * 100 as tip_pct
    from analytics.agg_hourly_demand
    where weather_category is not null
    group by 1
""")
st.subheader("Average tip % by weather")
st.bar_chart(tip.set_index("weather_category"))

daily = q("""
    select date_trunc('day', hour_ts) as day, sum(trips) as trips
    from analytics.agg_hourly_demand group by 1 order by 1
""")
st.subheader("Daily trips")
st.line_chart(daily.set_index("day"))