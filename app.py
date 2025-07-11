"""
Medicare Part D Drug Spending Dashboard

Professional dashboard inspired by 46brooklyn.com styling for analyzing 
Medicare Part D drug spending data from CMS.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html, get_asset_url
import dash_ag_grid as dag
from ag_grid_definition import component
import polars as pl
from dash.exceptions import PreventUpdate
from figure import create_partd_figure, aggregate_chart_data
from dash_iconify import DashIconify
from helpers import load_data
import io
import csv

app = Dash(
    external_stylesheets=dmc.styles.ALL,
    assets_folder='assets',
    title="Medicare Part D Drug Spending Dashboard"
)

server = app.server

# Create layout inspired by 46brooklyn design
layout = dmc.Container(
    [
        # Header Section - Professional 46Brooklyn Style
        dmc.Paper(
            [
            dmc.Stack(
                [
                dmc.Group(
                    [
                    dmc.Group(
                        [
                        # Brooklyn logo instead of pill icon
                        dmc.Image(
                            src="/assets/logo.png",
                            alt="46Brooklyn Logo",
                            w=100,
                            h=100,
                            fit="contain",
                            className="brooklyn-icon",
                            style={"filter": "drop-shadow(0 2px 4px rgba(0,0,0,0.1))"},
                          
                          
                        ),
                        dmc.Title(
                            "WHAT DRUGS COST IN MEDICARE PART D",
                            order=1,
                            className="main-title brooklyn-brand",
                            style={
                                "margin": 0,
                                "alignSelf": "center",
                                "fontSize": "2.25rem",
                                "fontWeight": 700,
                                "letterSpacing": "-0.025em",
                                "lineHeight": 1.2
                            }
                        ),
                        ],
                        gap="md",
                        align="center",
                    ),
                    dmc.Text(
                        "A comprehensive analysis of Medicare Part D drug spending patterns from 2013-2023",
                        className="subtitle",
                        style={
                            "textAlign": "left",
                            "marginTop": "0.5rem",
                            "fontSize": "1.125rem",
                            "color": "#4a5568",
                            "fontWeight": 400,
                            "lineHeight": 1.5
                        }
                    ),
                    dmc.Group(
                        [
                        dmc.Badge(
                            "Medicare Research",
                            variant="filled",
                            size="lg",
                            className="brooklyn-badge",
                            style={"fontWeight": 600}
                        ),
                        dmc.Badge(
                            "2013-2023 Data",
                            variant="outline",
                            size="lg",
                            className="brooklyn-badge-outline",
                            style={"fontWeight": 600}
                        ),
                        ],
                        gap="sm",
                    ),
                    ],
                    justify="space-between",
                    align="center",
                    wrap="wrap",
                ),
                ],
                gap="md",
            ),
            ],
            className="header-section",
            p="xl",
            radius="md",
            withBorder=True,
            mb="xl",
        ),
        
        # Clean Navigation Section with Modal Triggers
        dmc.Paper(
            [
                dmc.Group(
                    [
                        dmc.Button(
                            [
                                DashIconify(icon="tabler:info-circle", width=16),
                                "About This Dashboard"
                            ],
                            variant="light",
                            color="orange",
                            size="sm",
                            id="about-button",
                            className="brooklyn-button",
                        ),
                        dmc.Button(
                            [
                                DashIconify(icon="tabler:help", width=16),
                                "How to Use"
                            ],
                            variant="outline",
                            color="blue",
                            size="sm",
                            id="help-button",
                        ),
                        dmc.Button(
                            [
                                DashIconify(icon="tabler:chart-analytics", width=16),
                                "Key Insights"
                            ],
                            variant="outline",
                            color="blue",
                            size="sm",
                            id="insights-button",
                        ),
                        dmc.Button(
                            [
                                DashIconify(icon="tabler:database", width=16),
                                "Data Sources"
                            ],
                            variant="outline",
                            color="blue",
                            size="sm",
                            id="data-sources-button",
                        ),
                    ],
                    gap="sm",
                    justify="center",
                ),
            ],
            p="md",
            radius="md",
            className="brooklyn-paper",
            mb="lg",
            withBorder=True,
        ),

        # Modal Components
        dmc.Modal(
            title="About This Medicare Part D Analysis",
            id="about-modal",
            children=[
                dmc.Stack(
                    [
                        dmc.Text(
                            "This dashboard provides comprehensive analysis of Medicare Part D drug spending patterns from 2013-2023. "
                            "We've enhanced the raw CMS data with additional classifications and insights to make it easier for "
                            "researchers, policymakers, and the public to understand drug pricing trends in Medicare Part D.",
                            size="sm",
                        ),
                        dmc.Divider(),
                        dmc.Stack(
                            [
                                dmc.Group(
                                    [
                                        DashIconify(icon="tabler:database", width=20, color="#1a365d"),
                                        dmc.Text("Data Enhancement Process", fw="bold", className="brooklyn-brand"),
                                    ],
                                    gap="xs",
                                ),
                                dmc.List(
                                    [
                                        dmc.ListItem("Brand vs. Generic drug classifications using comprehensive pharmaceutical databases"),
                                        dmc.ListItem("Specialty drug flags based on CMS definition"),
                                        dmc.ListItem("Historical data preservation extending back to 2013 for trend analysis"),
                                        dmc.ListItem("Standardized format conversion from CMS Excel spreadsheets"),
                                    ],
                                    size="sm",
                                ),
                            ],
                            gap="xs",
                        ),
                    ],
                    gap="md",
                ),
            ],
            size="lg",
        ),

        dmc.Modal(
            title="How to Use This Dashboard",
            id="help-modal",
            children=[
                dmc.Stack(
                    [
                        dmc.Text(
                            "This interactive dashboard allows you to explore Medicare Part D drug spending data through multiple views:",
                            size="sm",
                            fw="bold",
                        ),
                        dmc.List(
                            [
                                dmc.ListItem("Use the data table below to filter and sort drugs by various criteria"),
                                dmc.ListItem("The chart automatically updates to show trends for your selected data"),
                                dmc.ListItem("Click column headers in the table to sort by different metrics"),
                                dmc.ListItem("Use the search and filter options to focus on specific drugs or categories"),
                                dmc.ListItem("Download filtered data as CSV using the 'Download CSV' button in the table header"),
                                dmc.ListItem("Export chart images using the toolbar in the top-right of the chart"),
                            ],
                            size="sm",
                        ),
                        dmc.Alert(
                            "Pro Tip: Try filtering by drug type or specialty status to see how different categories contribute to overall spending trends.",
                            title="Getting Started",
                            color="blue",
                            icon=DashIconify(icon="tabler:lightbulb"),
                        ),
                    ],
                    gap="md",
                ),
            ],
            size="xl",
        ),

        dmc.Modal(
            title="Key Insights from the Data",
            id="insights-modal",
            children=[
                dmc.Grid(
                    [
                        dmc.GridCol(
                            [
                                dmc.Paper(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        DashIconify(icon="tabler:trending-up", width=24, color="#1a365d"),
                                                        dmc.Text("Spending Trends", fw="bold", className="brooklyn-brand"),
                                                    ],
                                                    gap="xs",
                                                ),
                                                dmc.Text(
                                                    "Track Medicare Part D spending growth over time and identify "
                                                    "periods of significant change in drug costs and utilization patterns.",
                                                    size="sm",
                                                ),
                                            ],
                                            gap="xs",
                                        ),
                                    ],
                                    p="md",
                                    withBorder=True,
                                    className="brooklyn-paper",
                                ),
                            ],
                            span=6,
                        ),
                        dmc.GridCol(
                            [
                                dmc.Paper(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        DashIconify(icon="tabler:currency-dollar", width=24, color="#1a365d"),
                                                        dmc.Text("Cost Per Claim", fw="bold", className="brooklyn-brand"),
                                                    ],
                                                    gap="xs",
                                                ),
                                                dmc.Text(
                                                    "Analyze spending per claim trends to understand if cost increases "
                                                    "are driven by higher drug prices or increased utilization.",
                                                    size="sm",
                                                ),
                                            ],
                                            gap="xs",
                                        ),
                                    ],
                                    p="md",
                                    withBorder=True,
                                    className="brooklyn-paper",
                                ),
                            ],
                            span=6,
                        ),
                    ],
                    gutter="md",
                ),
            ],
            size="xl",
        ),

        dmc.Modal(
            title="Data Sources & Methodology",
            id="data-sources-modal",
            children=[
                dmc.Stack(
                    [
                        dmc.Grid(
                            [
                                dmc.GridCol(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Text("Primary Data Source", fw="bold", className="brooklyn-accent"),
                                                dmc.Text(
                                                    "Raw Medicare Part D spending data from the Centers for Medicare & Medicaid Services (CMS). "
                                                    "We maintain historical data extending back to 2013, including datasets no longer available "
                                                    "on the current CMS portal.",
                                                    size="sm",
                                                ),
                                                dmc.Anchor(
                                                    "CMS Medicare Part D Drug Spending Dashboard →",
                                                    href="https://data.cms.gov/tools/medicare-part-d-drug-spending-dashboard",
                                                    target="_blank",
                                                    size="sm",
                                                ),
                                            ],
                                            gap="xs",
                                        ),
                                    ],
                                    span=6,
                                ),
                                dmc.GridCol(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Text("Data Enhancement Process", fw="bold", className="brooklyn-accent"),
                                                dmc.List(
                                                    [
                                                        dmc.ListItem("Converted CMS Excel spreadsheets to standardized format"),
                                                        dmc.ListItem("Added drug type classifications (Brand, Generic, DME, Vaccine)"),
                                                        dmc.ListItem("Flagged specialty drugs using CMS criteria"),
                                                        dmc.ListItem("Calculated cost per beneficiary using total spending divided by beneficiaries"),
                                                    ],
                                                    size="sm",
                                                ),
                                            ],
                                            gap="xs",
                                        ),
                                    ],
                                    span=6,
                                ),
                            ],
                            gutter="md",
                        ),
                        dmc.Divider(),
                        dmc.Group(
                            [
                                dmc.Group(
                                    [
                                        DashIconify(icon="tabler:calendar", width=16, color="#ed8936"),
                                        dmc.Text("Update Frequency:", fw="bold", size="sm"),
                                        dmc.Text("Annual (when CMS releases new data)", size="sm"),
                                    ],
                                    gap="xs",
                                ),
                                dmc.Group(
                                    [
                                        DashIconify(icon="tabler:calendar-range", width=16, color="#ed8936"),
                                        dmc.Text("Coverage Period:", fw="bold", size="sm"),
                                        dmc.Text("2013-2023 (11 years)", size="sm"),
                                    ],
                                    gap="xs",
                                ),
                            ],
                            justify="space-between",
                            wrap="wrap",
                        ),
                    ],
                    gap="md",
                ),
            ],
            size="xl",
        ),

        # Chart Section - Professional Header
        dmc.Paper(
            [
                dmc.Stack(
                    [
                        # Chart Header
                        dmc.Group(
                            [
                                dmc.Group(
                                    [
                                        DashIconify(icon="tabler:chart-line", width=24, color="white"),
                                        dmc.Text(
                                            "Medicare Part D Spending Analysis",
                                            size="lg",
                                            fw="bold",
                                            className="brooklyn-card-header-title",
                                        ),
                                    ],
                                    gap="sm",
                                ),
                                dmc.Badge("Live Updates", color="orange", variant="light"),
                            ],
                            justify="space-between",
                            align="center",
                        ),
                    ],
                    gap="sm",
                ),
            ],
            className="brooklyn-card-header",
            p="md",
            mb=0,
        ),
        
        # Chart Container
        html.Div(
            [
                dcc.Graph(
                    id='fig',
                    config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'medicare_partd_spending_trends',
                            'height': 600,
                            'width': 1000,
                            'scale': 2
                        }
                    }
                )
            ],
            className="partd-chart-container",
        ),
        
        # Data Table Section - Professional Header with Download
        dmc.Paper(
            [
                dmc.Stack(
                    [
                        # Table Header
                        dmc.Group(
                            [
                                dmc.Group(
                                    [
                                        DashIconify(icon="tabler:table", width=24, color="white"),
                                        dmc.Text(
                                            "Detailed Drug Spending Database",
                                            size="lg",
                                            fw="bold",
                                            className="brooklyn-card-header-title",
                                        ),
                                    ],
                                    gap="sm",
                                ),
                                dmc.Group(
                                    [
                                        dmc.Badge("Filter & Sort", color="orange", variant="light"),
                                        dmc.Button(
                                            [
                                                DashIconify(icon="tabler:download", width=16),
                                                "Download CSV"
                                            ],
                                            variant="light",
                                            color="gray",
                                            size="sm",
                                            id="download-button",
                                            style={"color": "white", "backgroundColor": "rgba(255,255,255,0.2)"},
                                        ),
                                    ],
                                    gap="sm",
                                ),
                            ],
                            justify="space-between",
                            align="center",
                        ),
                    ],
                    gap="sm",
                ),
            ],
            className="brooklyn-card-header",
            p="md",
            mb=0,
        ),
        
        # AG Grid Component
        html.Div([component], className="brooklyn-card", style={"marginTop": 0, "paddingTop": 0}),
        
        # Download Component
        dcc.Download(id="download-csv"),
        
        
        
        # Clean Footer
        dmc.Paper(
            [
                dmc.Group(
                    [
                        dmc.Text(
                            "Dashboard methodology inspired by 46brooklyn.com's approach to Medicare Part D data analysis.",
                            size="xs",
                            c="gray",
                        ),
                        dmc.Anchor(
                            "CMS Data Source",
                            href="https://data.cms.gov/tools/medicare-part-d-drug-spending-dashboard",
                            target="_blank",
                            size="xs",
                        ),
                    ],
                    justify="space-between",
                    wrap="wrap",
                ),
            ],
            p="sm",
            radius="md",
            className="brooklyn-paper",
            mt="lg",
            style={"borderTop": "1px solid #e2e8f0"},
        ),
    ],
    size="xl",
    px="md",
    py="lg",
)

app.layout = dmc.MantineProvider(layout)


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