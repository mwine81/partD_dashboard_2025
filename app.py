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
from helpers import load_data, load_filtered_data
from UI.layout import layout


app = Dash(
    external_stylesheets=dmc.styles.ALL,
    assets_folder='assets',
    title="Medicare Part D Drug Spending Dashboard"
)

server = app.server

app.layout = dmc.MantineProvider(layout())

# Helper function to build filters dictionary
def build_filters_dict(product_name, generic_name, manufacturer, brand_generic_type, year_filter, specialty_filter):
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
    if year_filter:
        filters['year_filter'] = year_filter
    if specialty_filter and specialty_filter != "All":
        filters['specialty_filter'] = specialty_filter
    return filters

def create_no_data_figure(message="No data found for current selection"):
    """Create an informative figure when no data is available"""
    import plotly.graph_objects as go
    
    figure = go.Figure()
    figure.update_layout(
        title={
            'text': message,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#1a365d'}
        },
        xaxis_title="Year",
        yaxis_title="Total Spending",
        plot_bgcolor='white',
        paper_bgcolor='#f8fafc',
        height=600,
        annotations=[{
            'text': '💡 Try adjusting your filters to see data<br>or reset filters to view all data',
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.5,
            'y': 0.5,
            'xanchor': 'center',
            'yanchor': 'middle',
            'showarrow': False,
            'font': {'size': 16, 'color': '#718096'},
            'align': 'center'
        }]
    )
    return figure

def create_error_figure(error_message="An error occurred while loading data"):
    """Create an informative figure when an error occurs"""
    import plotly.graph_objects as go
    
    figure = go.Figure()
    figure.update_layout(
        title={
            'text': 'Error Loading Data',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#e53e3e'}
        },
        xaxis_title="Year",
        yaxis_title="Total Spending",
        plot_bgcolor='white',
        paper_bgcolor='#f8fafc',
        height=600,
        annotations=[{
            'text': f'⚠️ {error_message}<br>Please try again or contact support',
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.5,
            'y': 0.5,
            'xanchor': 'center',
            'yanchor': 'middle',
            'showarrow': False,
            'font': {'size': 16, 'color': '#e53e3e'},
            'align': 'center'
        }]
    )
    return figure

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
     State('year-filter', 'value'),
     State('specialty-filter', 'value')],
    prevent_initial_call=False
)
def update_data_and_chart(apply_clicks, reset_clicks, product_name, generic_name, 
                         manufacturer, brand_generic_type, year_filter, specialty_filter):
    """Update both grid data and chart based on applied filters"""
    
    try:
        # Determine which button was clicked (if any)
        ctx = callback_context
        
        # Reset filters if reset button was clicked
        if ctx and ctx.triggered and 'reset-filters-btn' in ctx.triggered[0]['prop_id']:
            # Load all data when reset
            filtered_data = load_data().collect()
        else:
            # Build filters dictionary
            filters = build_filters_dict(product_name, generic_name, manufacturer, 
                                       brand_generic_type, year_filter, specialty_filter)
            
            # Get filtered data
            if filters:
                filtered_data = load_filtered_data(
                    product_name=filters.get('product_name'),
                    generic_name=filters.get('generic_name'),
                    manufacturer=filters.get('manufacturer'),
                    brand_generic_type=filters.get('brand_generic_type'),
                    year_filter=filters.get('year_filter'),
                    specialty_filter=filters.get('specialty_filter')
                ).collect()
            else:
                # No filters applied, load all data
                filtered_data = load_data().collect()
        
        # Check if data exists
        if filtered_data.height == 0:
            # Return empty data with helpful message
            return [], create_no_data_figure("No data matches your current filter selection")
        
        # Prepare data for AG Grid
        grid_data = filtered_data.to_dicts()
        
        # Prepare data for chart
        chart_data = aggregate_chart_data(filtered_data)
        figure = create_partd_figure(chart_data)
        
        return grid_data, figure
        
    except Exception as e:
        print(f"Error in update_data_and_chart: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error state with helpful message
        error_msg = "Data processing error occurred"
        if "FileNotFoundError" in str(e):
            error_msg = "Data file not found"
        elif "ParquetError" in str(e):
            error_msg = "Data file format error"
        
        return [], create_error_figure(error_msg)

# Reset filters callback
@callback(
    [Output('product-filter', 'value'),
     Output('generic-filter', 'value'),
     Output('manufacturer-filter', 'value'),
     Output('type-filter', 'value'),
     Output('year-filter', 'value'),
     Output('specialty-filter', 'value')],
    Input('reset-filters-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    """Reset all filter values to their defaults"""
    return None, None, None, None, None, "All"

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

# Download callback - now uses current grid data with better UX
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
            
            # Add helpful metadata as comments
            current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            record_count = len(df_pandas)
            
            # Create enhanced CSV with metadata header
            csv_lines = [
                f"# Medicare Part D Drug Spending Data Export",
                f"# Generated: {current_time}",
                f"# Records: {record_count:,}",
                f"# Filters: Applied (showing filtered results)",
                f"# Data Source: CMS Part D Drug Spending Dashboard",
                f"#",
            ]
            
            # Add the actual CSV data
            csv_content = "\n".join(csv_lines) + "\n" + df_pandas.to_csv(index=False)
            
            filename = f"medicare_partd_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        else:
            # Fallback to loading all data if no grid data
            df = load_data().collect()
            df_pandas = df.to_pandas()
            
            current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            record_count = len(df_pandas)
            
            csv_lines = [
                f"# Medicare Part D Drug Spending Data Export",
                f"# Generated: {current_time}",
                f"# Records: {record_count:,}",
                f"# Filters: None (showing all data)",
                f"# Data Source: CMS Part D Drug Spending Dashboard",
                f"#",
            ]
            
            csv_content = "\n".join(csv_lines) + "\n" + df_pandas.to_csv(index=False)
            filename = f"medicare_partd_complete_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return dict(
            content=csv_content,
            filename=filename,
            type="text/csv"
        )
    
    except Exception as e:
        print(f"Error in CSV download: {e}")
        import traceback
        traceback.print_exc()
        
        # Return helpful error file
        error_content = f"""# Medicare Part D Data Export - Error Report
# Generated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}
# Status: Export Failed
# Error: {str(e)}
#
# Please try the following:
# 1. Refresh the page and try again
# 2. Check your internet connection
# 3. Contact support if the problem persists
#
# Error Details:
{str(e)}
"""
        return dict(
            content=error_content,
            filename=f"export_error_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
            type="text/plain"
        )

# Client-side callback to show filter status
app.clientside_callback(
    """
    function(product, generic, manufacturer, type, year, specialty) {
        // Check if any filters are active
        const hasFilters = (product && product.length > 0) ||
                          (generic && generic.length > 0) ||
                          (manufacturer && manufacturer.length > 0) ||
                          (type && type.length > 0) ||
                          (year && year.length > 0) ||
                          (specialty && specialty !== "All" && specialty !== "all");
        
        if (hasFilters) {
            return {
                'display': 'inline-flex',
                'backgroundColor': '#fed7aa',
                'color': '#c05621',
                'animation': 'pulse 2s infinite'
            };
        } else {
            return {'display': 'none'};
        }
    }
    """,
    Output('filter-status-badge', 'style'),
    [Input('product-filter', 'value'),
     Input('generic-filter', 'value'),
     Input('manufacturer-filter', 'value'),
     Input('type-filter', 'value'),
     Input('year-filter', 'value'),
     Input('specialty-filter', 'value')]
)

if __name__ == "__main__":
    app.run(debug=True)