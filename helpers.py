import polars as pl
from polars import col as c
import polars.selectors as cs
from pathlib import Path

def load_data():
    data_path = Path(__file__).parent / "data" / "partD.parquet"
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    return pl.scan_parquet(data_path)


if __name__ == "__main__":
    pass
