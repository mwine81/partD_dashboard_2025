import dash_mantine_components as dmc
import polars as pl
from polars import col as c
import polars.selectors as cs
from pathlib import Path
from dash_iconify import DashIconify
from helpers import load_data

def load_choices(col_name: str) -> list:
    data = load_data()
    choices = data.select(cs.matches(f'(?i){col_name}').unique().sort()).collect().to_series().to_list()
    return choices

def get_min_and_max_years() -> tuple:
    data = load_data()
    min_year = data.select(c("YEAR").min()).collect().item()
    max_year = data.select(c("YEAR").max()).collect().item()
    return min_year, max_year

def create_dropdown(col_name: str, label: str, component_id: str) -> dmc.MultiSelect:
    return dmc.MultiSelect(
        data=load_choices(col_name),
        value=None,
        label=label,
        id=component_id,
        placeholder=f"Select {label}...",
        searchable=True,
        clearable=True,
        style={"minWidth": "200px"}
    )

def create_year_filter() -> dmc.MultiSelect:
    min_year, max_year = get_min_and_max_years()
    year_options = [str(year) for year in range(min_year, max_year + 1)]
    return dmc.MultiSelect(
        data=year_options,
        value=None,  # No filter by default
        label="Year Selection",
        id="year-filter",
        placeholder="Select years (leave empty for all years)...",
        searchable=True,
        clearable=True,
        style={"minWidth": "200px"}
    )

def create_specialty_filter() -> dmc.Stack:
    return dmc.Stack([
        dmc.Text("Specialty Drug Filter", size="sm", fw="bold"),
        dmc.SegmentedControl(
            id="specialty-filter",
            value="all",
            data=[
                "All",
                "Specialty Only", 
                "Non-Specialty Only"
            ],
            size="sm",
            radius="md"
        )
    ], gap="xs")

def create_filters() -> dmc.Paper:
    return dmc.Paper([
        dmc.Stack([
            # Filter Header with Status
            dmc.Group([
                dmc.Group([
                    DashIconify(icon="tabler:filter", width=20, color="#1a365d"),
                    dmc.Text("Data Filters", size="lg", fw="bold", style={"color": "#1a365d"})
                ], gap="xs"),
                dmc.Group([
                    dmc.Badge(
                        "Filters Active",
                        id="filter-status-badge", 
                        color="orange", 
                        variant="light",
                        style={"display": "none"}  # Hidden by default
                    ),
                    dmc.Button(
                        [DashIconify(icon="tabler:refresh", width=16), "Reset Filters"],
                        variant="outline",
                        color="gray",
                        size="sm",
                        id="reset-filters-btn"
                    )
                ], gap="sm")
            ], justify="space-between", align="center"),
            
            dmc.Divider(),
            
            # User guidance
            dmc.Alert(
                [
                    DashIconify(icon="tabler:info-circle", width=16),
                    " Select filters below to narrow your data analysis. Leave empty to view all data."
                ],
                color="blue",
                variant="light"
            ),
            
            # Filter Controls
            dmc.Grid([
                # Dropdown Filters - Row 1
                dmc.GridCol([
                    create_dropdown("Product_Name", "Product Name", "product-filter")
                ], span=4),
                dmc.GridCol([
                    create_dropdown("Generic_Name", "Generic Name", "generic-filter")
                ], span=4),
                dmc.GridCol([
                    create_dropdown("Manufacturer", "Manufacturer", "manufacturer-filter")
                ], span=4),
                
                # Dropdown Filters - Row 2
                dmc.GridCol([
                    create_dropdown("Brand_vs_Generic", "Brand/Generic", "type-filter")
                ], span=4),
                
                # Year Filter
                dmc.GridCol([
                    create_year_filter()
                ], span=4),
                
                # Specialty Drug Filter
                dmc.GridCol([
                    create_specialty_filter()
                ], span=4),
            ], gutter="md"),
            
            # Apply Filters Button with enhanced styling
            dmc.Group([
                dmc.Button(
                    [DashIconify(icon="tabler:search", width=16), "Apply Filters"],
                    id="apply-filters-btn",
                    variant="filled",
                    size="md",
                    style={
                        "backgroundColor": "#1a365d",
                        "border": "2px solid #1a365d",
                        "transition": "all 0.2s ease"
                    },
                    fullWidth=False
                ),
                dmc.Tooltip(
                    label="Charts and tables update automatically when you apply filters",
                    position="top",
                    withArrow=True,
                    children=[
                        DashIconify(
                            icon="tabler:info-circle", 
                            width=20, 
                            color="#718096",
                            style={"cursor": "help", "marginLeft": "8px"}
                        )
                    ]
                )
            ], justify="center", align="center", gap="xs", mt="md")
        ], gap="md")
    ], 
    p="lg", 
    radius="md", 
    withBorder=True, 
    mb="lg",
    style={
        "border": "1px solid #e2e8f0",
        "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.05)",
        "transition": "all 0.2s ease"
    })





