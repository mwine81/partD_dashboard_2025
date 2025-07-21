import polars as pl
from polars import col as c
import polars.selectors as cs
from pathlib import Path
from typing import Optional, List, Tuple

def load_data():
    data_path = Path(__file__).parent / "data" / "partd.parquet"
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    return pl.scan_parquet(data_path)

def load_filtered_data(
    product_name: Optional[List[str]] = None,
    generic_name: Optional[List[str]] = None, 
    manufacturer: Optional[List[str]] = None,
    brand_generic_type: Optional[List[str]] = None,
    year_filter: Optional[List[str]] = None,
    specialty_filter: Optional[str] = None
) -> pl.LazyFrame:
    """
    Load data with applied filters for efficient querying.
    
    Args:
        product_name: Filter by product name(s)
        generic_name: Filter by generic name(s)
        manufacturer: Filter by manufacturer(s)
        brand_generic_type: Filter by brand/generic type(s)
        year_filter: List of years to filter by (e.g., ['2020', '2021'])
        specialty_filter: 'All', 'Specialty Only', or 'Non-Specialty Only'
    
    Returns:
        Filtered LazyFrame ready for collection
    """
    query = load_data()
    
    # Apply filters only if values are provided
    if product_name:
        query = query.filter(c("Product_Name").is_in(product_name))
    
    if generic_name:
        query = query.filter(c("Generic_Name").is_in(generic_name))
    
    if manufacturer:
        query = query.filter(c("Manufacturer").is_in(manufacturer))
    
    if brand_generic_type:
        query = query.filter(c("Brand_vs_Generic").is_in(brand_generic_type))
    
    if year_filter:
        # Convert string years to integers for filtering
        year_ints = [int(year) for year in year_filter]
        query = query.filter(c("YEAR").is_in(year_ints))
    
    if specialty_filter and specialty_filter != "All":
        if specialty_filter == "Specialty Only":
            query = query.filter(c("SPECIALTY_DRUG") == True)
        elif specialty_filter == "Non-Specialty Only":
            query = query.filter(c("SPECIALTY_DRUG") == False)
    
    return query

def get_filtered_data_for_grid(filters: dict) -> List[dict]:
    """
    Get filtered data formatted for AG Grid.
    
    Args:
        filters: Dictionary containing filter values
    
    Returns:
        List of dictionaries for AG Grid rowData
    """
    query = load_filtered_data(
        product_name=filters.get('product_name'),
        generic_name=filters.get('generic_name'),
        manufacturer=filters.get('manufacturer'),
        brand_generic_type=filters.get('brand_generic_type'),
        year_filter=filters.get('year_filter'),
        specialty_filter=filters.get('specialty_filter')
    )
    
    return query.collect().to_dicts()

if __name__ == "__main__":
    pass
