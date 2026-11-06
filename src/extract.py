import logging
from pathlib import Path

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

YEAR, MONTH = 2024, 1
BASE = "https://d37ci6vzurychx.cloudfront.net"
TAXI_URL = f"{BASE}/trip-data/yellow_tripdata_{YEAR}-{MONTH:02d}.parquet"
ZONES_URL = f"{BASE}/misc/taxi_zone_lookup.csv"
WEATHER_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=40.71&longitude=-74.01"
    f"&start_date={YEAR}-{MONTH:02d}-01&end_date={YEAR}-{MONTH:02d}-31"
    "&hourly=temperature_2m,precipitation,wind_speed_10m"
    "&timezone=America/New_York"
)


def download(url: str, dest: Path) -> None:
    """Download a file. Skips if it already exists (idempotent)."""
    if dest.exists():
        logger.info("Skipping %s (already exists)", dest.name)
        return
    logger.info("Downloading %s", url)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.writelines(r.iter_content(chunk_size=1024 * 1024))


def fetch_weather(dest: Path) -> None:
    if dest.exists():
        logger.info("Skipping %s (already exists)", dest.name)
        return
    r = requests.get(WEATHER_URL, timeout=60)
    r.raise_for_status()
    hourly = r.json()["hourly"]
    df = pd.DataFrame(hourly).rename(columns={"time": "hour_ts"})
    df.to_csv(dest, index=False)
    logger.info("Saved %d weather rows", len(df))


if __name__ == "__main__":
    download(TAXI_URL, RAW_DIR / "taxi.parquet")
    download(ZONES_URL, RAW_DIR / "zones.csv")
    fetch_weather(RAW_DIR / "weather.csv")
    taxi = pd.read_parquet(RAW_DIR / "taxi.parquet")
    logger.info("Taxi rows: %d, columns: %d", *taxi.shape)