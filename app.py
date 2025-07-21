"""
Medicare Part D Drug Spending Dashboard

Professional dashboard inspired by 46brooklyn.com styling for analyzing 
Medicare Part D drug spending data from CMS.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback
import polars as pl
from dash.exceptions import PreventUpdate
from figure import create_partd_figure, aggregate_chart_data
from helpers import load_data
from UI.layout import layout

app = Dash(
    external_stylesheets=dmc.styles.ALL,
    assets_folder='assets',
    title="Medicare Part D Drug Spending Dashboard"
)

server = app.server

app.layout = dmc.MantineProvider(layout())


@callback(
    Output('fig', 'figure'),
    Input('ag-grid', 'virtualRowData')
)
def update_fig(virtual_row_data):
    if not virtual_row_data:
        raise PreventUpdate
        
    try:
        data = pl.DataFrame(
            virtual_row_data, 
            strict=False
        )
    except Exception as e:
        print(f"Error updating visualizations: {e}")
        raise PreventUpdate
    data = aggregate_chart_data(data)
    fig = create_partd_figure(data)
    return fig

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

# Download callback
@callback(
    Output("download-csv", "data"),
    Input("download-button", "n_clicks"),
    State("ag-grid", "virtualRowData"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, virtual_row_data):
    if n_clicks is None:
        raise PreventUpdate
    
    # If there's filtered data, use that; otherwise use all data
    if virtual_row_data:
        df = pl.DataFrame(virtual_row_data, strict=False)
    else:
        df = load_data().collect()
    
    # Convert to pandas for easier CSV export
    df_pandas = df.to_pandas()
    
    # Create CSV string
    csv_string = df_pandas.to_csv(index=False)
    
    return dict(
        content=csv_string,
        filename="medicare_partd_drug_spending.csv"
    )

if __name__ == "__main__":
    app.run(debug=True)