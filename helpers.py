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
    year_range: Optional[Tuple[int, int]] = None,
    specialty_filter: Optional[str] = None
) -> pl.LazyFrame:
    """
    Load data with applied filters for efficient querying.
    
    Args:
        product_name: Filter by product name(s)
        generic_name: Filter by generic name(s)
        manufacturer: Filter by manufacturer(s)
        brand_generic_type: Filter by brand/generic type(s)
        year_range: Tuple of (min_year, max_year) for year filtering
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
    
    if year_range and len(year_range) == 2:
        min_year, max_year = year_range
        query = query.filter(c("YEAR").is_between(min_year, max_year))
    
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
        year_range=filters.get('year_range'),
        specialty_filter=filters.get('specialty_filter')
    )
    
    return query.collect().to_dicts()

if __name__ == "__main__":
    pass
