import polars as pl
from polars import col as c
import polars.selectors as cs

def load_data():
    return pl.scan_parquet("data/partD.parquet")


if __name__ == "__main__":
    pass
