from src.extract import TAXI_URL, ZONES_URL


def test_taxi_url_is_parquet():
    assert TAXI_URL.endswith(".parquet")


def test_zones_url_is_csv():
    assert ZONES_URL.endswith(".csv")