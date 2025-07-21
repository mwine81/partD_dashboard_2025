"""
Medicare Part D Drug Spending Dashboard

Professional dashboard inspired by 46brooklyn.com styling for analyzing 
Medicare Part D drug spending data from CMS.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, callback_context
import polars as pl
import pandas as pd
from dash.exceptions import PreventUpdate
from figures.figure import create_partd_figure, aggregate_chart_data
from helpers import load_data, load_filtered_data, get_filtered_data_for_grid
from UI.layout import layout


app = Dash(
    external_stylesheets=dmc.styles.ALL,
    assets_folder='assets',
    title="Medicare Part D Drug Spending Dashboard"
)

server = app.server

app.layout = dmc.MantineProvider(layout())

# Helper function to build filters dictionary
def build_filters_dict(product_name, generic_name, manufacturer, brand_generic_type, year_range, specialty_filter):
    """Build filters dictionary from callback inputs"""
    filters = {}
    if product_name:
        filters['product_name'] = product_name
    if generic_name:
        filters['generic_name'] = generic_name
    if manufacturer:
        filters['manufacturer'] = manufacturer
    if brand_generic_type:
        filters['brand_generic_type'] = brand_generic_type
    if year_range:
        filters['year_range'] = year_range
    if specialty_filter:
        filters['specialty_filter'] = specialty_filter
    return filters

# Main callback to update both grid and figure based on filters
@callback(
    [Output('ag-grid', 'rowData'),
     Output('fig', 'figure')],
    [Input('apply-filters-btn', 'n_clicks'),
     Input('reset-filters-btn', 'n_clicks')],
    [State('product-filter', 'value'),
     State('generic-filter', 'value'),
     State('manufacturer-filter', 'value'),
     State('type-filter', 'value'),
     State('year-range-slider', 'value'),
     State('specialty-filter', 'value')],
    prevent_initial_call=False
)
def update_data_and_chart(apply_clicks, reset_clicks, product_name, generic_name, 
                         manufacturer, brand_generic_type, year_range, specialty_filter):
    """Update both grid data and chart based on applied filters"""
    
    # Determine which button was clicked (if any)
    ctx = callback_context
    
    # Reset filters if reset button was clicked
    if ctx and ctx.triggered and 'reset-filters-btn' in ctx.triggered[0]['prop_id']:
        # Load all data when reset
        filters = {}
        filtered_data = load_data().collect()
    else:
        # Build filters dictionary
        filters = build_filters_dict(product_name, generic_name, manufacturer, 
                                   brand_generic_type, year_range, specialty_filter)
        
        # Get filtered data
        if filters:
            filtered_data = load_filtered_data(
                product_name=filters.get('product_name'),
                generic_name=filters.get('generic_name'),
                manufacturer=filters.get('manufacturer'),
                brand_generic_type=filters.get('brand_generic_type'),
                year_range=filters.get('year_range'),
                specialty_filter=filters.get('specialty_filter')
            ).collect()
        else:
            # No filters applied, load all data
            filtered_data = load_data().collect()
    
    # Prepare data for AG Grid
    grid_data = filtered_data.to_dicts()
    
    # Prepare data for chart
    try:
        chart_data = aggregate_chart_data(filtered_data)
        figure = create_partd_figure(chart_data)
    except Exception as e:
        print(f"Error creating chart: {e}")
        # Return empty figure if there's an error
        import plotly.graph_objects as go
        figure = go.Figure()
        figure.update_layout(
            title="No data available for current filters",
            xaxis_title="Year",
            yaxis_title="Total Spending"
        )
    
    return grid_data, figure

# Reset filters callback
@callback(
    [Output('product-filter', 'value'),
     Output('generic-filter', 'value'),
     Output('manufacturer-filter', 'value'),
     Output('type-filter', 'value'),
     Output('year-range-slider', 'value'),
     Output('specialty-filter', 'value')],
    Input('reset-filters-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    """Reset all filter values to their defaults"""
    # Get min/max years for slider reset
    from UI.select import get_min_and_max_years
    min_year, max_year = get_min_and_max_years()
    
    return None, None, None, None, (min_year, max_year), "All"

# Modal callbacks
@callback(
    Output("about-modal", "opened"),
    Input("about-button", "n_clicks"),
    prevent_initial_call=True,
)
def open_about_modal(n_clicks):
    return True

@callback(
    Output("help-modal", "opened"),
    Input("help-button", "n_clicks"),
    prevent_initial_call=True,
)
def open_help_modal(n_clicks):
    return True

@callback(
    Output("insights-modal", "opened"),
    Input("insights-button", "n_clicks"),
    prevent_initial_call=True,
)
def open_insights_modal(n_clicks):
    return True

@callback(
    Output("data-sources-modal", "opened"),
    Input("data-sources-button", "n_clicks"),
    prevent_initial_call=True,
)
def open_data_sources_modal(n_clicks):
    return True

# Download callback - now uses current grid data
@callback(
    Output("download-csv", "data"),
    Input("download-button", "n_clicks"),
    State("ag-grid", "rowData"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, row_data):
    if n_clicks is None:
        raise PreventUpdate
    
    try:
        # Use current grid data for download
        if row_data and len(row_data) > 0:
            # Convert list of dicts directly to pandas
            df_pandas = pd.DataFrame(row_data)
        else:
            # Fallback to loading all data if no grid data
            df = load_data().collect()
            df_pandas = df.to_pandas()
        
        # Create CSV string
        csv_string = df_pandas.to_csv(index=False)
        
        return dict(
            content=csv_string,
            filename="medicare_partd_drug_spending_filtered.csv",
            type="text/csv"
        )
    
    except Exception as e:
        print(f"Error in CSV download: {e}")
        # Return empty file as fallback
        return dict(
            content="Error generating CSV file",
            filename="error.txt",
            type="text/plain"
        )

if __name__ == "__main__":
    app.run(debug=True)