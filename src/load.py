import logging
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

url = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(url)

TAXI_COLS = [
    "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
    "passenger_count", "trip_distance", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "tip_amount", "total_amount",
]


def load_table(df: pd.DataFrame, name: str) -> None:
    # if_exists="replace" makes the load idempotent: re-running gives the same result
    df.to_sql(name, engine, schema="raw", if_exists="replace",
              index=False, chunksize=50_000)
    logger.info("Loaded %d rows into raw.%s", len(df), name)


if __name__ == "__main__":
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    taxi = pd.read_parquet("data/raw/taxi.parquet", columns=TAXI_COLS)
    load_table(taxi, "taxi_trips")
    load_table(pd.read_csv("data/raw/zones.csv"), "zones")
    weather = pd.read_csv("data/raw/weather.csv", parse_dates=["hour_ts"])
    load_table(weather, "weather")