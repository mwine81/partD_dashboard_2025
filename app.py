"""
Medicare Part D Drug Spending Dashboard

Professional dashboard inspired by 46brooklyn.com styling for analyzing 
Medicare Part D drug spending data from CMS.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html, get_asset_url
from ag_grid_definition import component
import polars as pl
from dash.exceptions import PreventUpdate
from figure import create_partd_figure, aggregate_chart_data
from dash_iconify import DashIconify

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
        
        # Instructions Section
        dmc.Paper(
            [
                dmc.Group(
                    [
                        DashIconify(icon="tabler:info-circle", width=20, color="#ed8936"),
                        dmc.Text("How to Use This Dashboard", fw="bold", className="brooklyn-accent"),
                    ],
                    gap="xs",
                    mb="sm",
                ),
                dmc.Text(
                    "Explore Medicare Part D drug spending data through the interactive table below. Filter and sort the data to analyze spending patterns, then view the dynamic chart that updates based on your selections.",
                    size="sm",
                    c="dark",
                ),
            ],
            p="md",
            radius="md",
            className="brooklyn-paper-orange",
            mb="lg",
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
        
        # Data Table Section - Professional Header
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
                                dmc.Badge("Filter & Sort", color="orange", variant="light"),
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
        
        
        
        # Footer Section
        dmc.Paper(
            [
                dmc.Stack(
                    [
                        dmc.Group(
                            [
                                dmc.Text("Data Source:", size="sm", fw="bold", className="brooklyn-brand"),
                                dmc.Anchor(
                                    "CMS Medicare Part D Drug Spending Dashboard",
                                    href="https://data.cms.gov/tools/medicare-part-d-drug-spending-dashboard",
                                    target="_blank",
                                    size="sm",
                                    c="blue",
                                ),
                            ],
                            gap="xs",
                            align="center",
                        ),
                        dmc.Text(
                            "Dashboard inspired by 46brooklyn.com design principles for professional healthcare data visualization.",
                            size="xs",
                            c="gray",
                            ta="center",
                        ),
                    ],
                    gap="xs",
                ),
            ],
            p="md",
            radius="md",
            className="brooklyn-paper",
            mt="xl",
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

if __name__ == "__main__":
    app.run(debug=True)