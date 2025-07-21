import dash_mantine_components as dmc
import polars as pl
from polars import col as c
import polars.selectors as cs
from pathlib import Path

def load_choices(col_name: str) -> list:
    data = pl.scan_parquet(Path("data/partd.parquet"))
    choices = data.select(cs.matches(f'(?i){col_name}').unique().sort()).collect().to_series().to_list()
    return choices

def get_min_and_max_years() -> tuple:
    data = pl.scan_parquet(Path("data/partd.parquet"))
    min_year = data.select(c.YEAR.min()).collect(engine='streaming').item()
    max_year = data.select(c.YEAR.max()).collect(engine='streaming').item()
    return min_year, max_year

def create_dropdown(col_name: str, label: str) -> dmc.Select:
    return dmc.Select(
        data=load_choices(col_name),
        value=None,
        label=label
    )

def create_year_slider() -> dmc.RangeSlider:
    min_year, max_year = get_min_and_max_years()
    return dmc.RangeSlider(
        min=min_year,
        max=max_year,
        step=1,
        value=(2015, 2023),
        marks=[{"value": year, "label": str(year)} for year in range(2015, 2024)],
        label="Year Range",
        size="md"
    )



def create_filters() -> dmc.Group:
    return dmc.Group([
        create_dropdown("Product_Name", "Product Name"),
        create_dropdown("Generic_Name", "Generic Name"),
        create_dropdown("Manufacturer", "Manufacturer"),

    ])





