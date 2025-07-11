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
        # Header Section - Clean Minimalist Design
        dmc.Paper(
            [
                dmc.Stack(
                    [
                        # Main Header Row
                        dmc.Group(
                            [
                                # Left Side - Logo and Branding
                                dmc.Group(
                                    [
                                        html.Img(
                                            src=get_asset_url("logo2.png"),
                                            style={
                                                "height": "60px",
                                                "width": "auto",
                                                "objectFit": "contain"
                                            }
                                        ),
                                        dmc.Stack(
                                            [
                                                dmc.Text(
                                                    "Medicare Part D",
                                                    size="xs",
                                                    tt="uppercase",
                                                    fw="bold",
                                                    c="gray",
                                                    style={"letterSpacing": "0.1em"}
                                                ),
                                                dmc.Title(
                                                    "Drug Spending Analytics",
                                                    order=2,
                                                    style={
                                                        "fontWeight": 600,
                                                        "fontSize": "1.75rem",
                                                        "lineHeight": 1.2,
                                                        "margin": 0,
                                                        "color": "#1a365d"
                                                    }
                                                ),
                                            ],
                                            gap=0,
                                        ),
                                    ],
                                    gap="md",
                                    align="center",
                                ),
                                
                                # Right Side - Key Stats
                                dmc.Group(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Text("Data Period", size="xs", c="gray", ta="center"),
                                                dmc.Text(
                                                    "2013-2023", 
                                                    size="lg", 
                                                    fw="bold", 
                                                    ta="center",
                                                    style={"color": "#1a365d"}
                                                ),
                                            ],
                                            gap=2,
                                        ),
                                        dmc.Divider(orientation="vertical", style={"height": "40px"}),
                                        dmc.Stack(
                                            [
                                                dmc.Text("Data Source", size="xs", c="gray", ta="center"),
                                                dmc.Text(
                                                    "CMS", 
                                                    size="lg", 
                                                    fw="bold", 
                                                    ta="center",
                                                    style={"color": "#ed8936"}
                                                ),
                                            ],
                                            gap=2,
                                        ),
                                        dmc.Divider(orientation="vertical", style={"height": "40px"}),
                                        dmc.Stack(
                                            [
                                                dmc.Text("Records", size="xs", c="gray", ta="center"),
                                                dmc.Text(
                                                    "90K+", 
                                                    size="lg", 
                                                    fw="bold", 
                                                    ta="center",
                                                    style={"color": "#1a365d"}
                                                ),
                                            ],
                                            gap=2,
                                        ),
                                    ],
                                    gap="lg",
                                    align="center",
                                ),
                            ],
                            justify="space-between",
                            align="center",
                            wrap="wrap",
                        ),
                        
                        # Subtitle Section
                        dmc.Text(
                            "Comprehensive analysis of Medicare Part D drug spending patterns with enhanced CMS data classifications",
                            size="md",
                            c="gray",
                            ta="center",
                            style={"maxWidth": "700px", "margin": "0 auto"}
                        ),
                        
                        # Status Indicators
                        dmc.Group(
                            [
                                dmc.Badge(
                                    [
                                        DashIconify(icon="tabler:circle-check", width=12),
                                        "Live Data"
                                    ],
                                    variant="dot",
                                    color="green",
                                    size="sm",
                                ),
                                dmc.Badge(
                                    [
                                        DashIconify(icon="tabler:shield-check", width=12),
                                        "CMS Verified"
                                    ],
                                    variant="dot",
                                    color="blue",
                                    size="sm",
                                ),
                                dmc.Badge(
                                    [
                                        DashIconify(icon="tabler:clock", width=12),
                                        "Updated 2025"
                                    ],
                                    variant="dot",
                                    color="orange",
                                    size="sm",
                                ),
                            ],
                            justify="center",
                            gap="lg",
                        ),
                    ],
                    gap="md",
                ),
            ],
            p="xl",
            radius="lg",
            withBorder=False,
            mb="lg",
            style={
                "background": "linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #ffffff 100%)",
                "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1)",
                "border": "1px solid #e2e8f0",
            }
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
            title="About Medicare Part D Drug Spending Data",
            id="about-modal",
            children=[
                dmc.Stack(
                    [
                        dmc.Text(
                            "The Part D Drug Spending Dashboard presents information on spending for drugs prescribed to Medicare beneficiaries enrolled in Part D by physicians and other healthcare providers. This data is sourced from Part D Prescription Drug Event (PDE) records and provides comprehensive insights into Medicare prescription drug costs.",
                            size="sm",
                        ),
                        dmc.Divider(),
                        dmc.Stack(
                            [
                                dmc.Group(
                                    [
                                        DashIconify(icon="tabler:database", width=20, color="#1a365d"),
                                        dmc.Text("Data Source & Processing", fw="bold", className="brooklyn-brand"),
                                    ],
                                    gap="xs",
                                ),
                                dmc.List(
                                    [
                                        dmc.ListItem("Part D Prescription Drug Event (PDE) data from CMS"),
                                        dmc.ListItem("National Drug Codes (NDCs) linked to commercial databases"),
                                        dmc.ListItem("Aggregated across all strengths, dosage forms, and routes of administration"),
                                        dmc.ListItem("Includes all Part D organization and plan types"),
                                        dmc.ListItem("Excludes over-the-counter drugs and drugs with fewer than 11 claims"),
                                    ],
                                    size="sm",
                                ),
                            ],
                            gap="xs",
                        ),
                        dmc.Divider(),
                        dmc.Stack(
                            [
                                dmc.Group(
                                    [
                                        DashIconify(icon="tabler:currency-dollar", width=20, color="#ed8936"),
                                        dmc.Text("Drug Spending Metrics", fw="bold", className="brooklyn-accent"),
                                    ],
                                    gap="xs",
                                ),
                                dmc.Text(
                                    "Drug spending is based on gross drug cost, which includes ingredient cost, dispensing fees, sales tax, and applicable vaccine administration fees. This represents total spending including amounts paid by Medicare Part D plans and beneficiary payments.",
                                    size="sm",
                                ),
                                dmc.Alert(
                                    "Note: Part D spending metrics do not reflect manufacturers' rebates or other price concessions as CMS is prohibited from publicly disclosing such information.",
                                    color="orange",
                                    icon=DashIconify(icon="tabler:info-circle"),
                                ),
                            ],
                            gap="xs",
                        ),
                    ],
                    gap="md",
                ),
            ],
            size="xl",
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
            title="Key Insights & Methodology",
            id="insights-modal",
            children=[
                dmc.Stack(
                    [
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
                                                                DashIconify(icon="tabler:calculator", width=24, color="#1a365d"),
                                                                dmc.Text("Average Spending per Dosage Unit", fw="bold", className="brooklyn-brand"),
                                                            ],
                                                            gap="xs",
                                                        ),
                                                        dmc.Text(
                                                            "Part D drug spending divided by the number of dosage units, weighted by the proportion of total claims. This accounts for variation in claims volume across different strengths, dosage forms, and manufacturers.",
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
                                                                DashIconify(icon="tabler:trending-up", width=24, color="#1a365d"),
                                                                dmc.Text("Annual Growth Rate Analysis", fw="bold", className="brooklyn-brand"),
                                                            ],
                                                            gap="xs",
                                                        ),
                                                        dmc.Text(
                                                            "The constant average change in spending per dosage unit over the most recent five years, calculated using compound annual growth rate (CAGR) methodology.",
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
                                                                DashIconify(icon="tabler:users", width=24, color="#ed8936"),
                                                                dmc.Text("Beneficiary Impact Analysis", fw="bold", className="brooklyn-accent"),
                                                            ],
                                                            gap="xs",
                                                        ),
                                                        dmc.Text(
                                                            "Average spending per beneficiary calculated as total Part D drug spending divided by the number of unique beneficiaries utilizing each drug during the benefit year.",
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
                                                                DashIconify(icon="tabler:alert-triangle", width=24, color="#ed8936"),
                                                                dmc.Text("Outlier Detection", fw="bold", className="brooklyn-accent"),
                                                            ],
                                                            gap="xs",
                                                        ),
                                                        dmc.Text(
                                                            "Drugs marked with '^' are identified as outliers due to potentially anomalous dosage unit values that may misrepresent average spending calculations. Exercise caution when interpreting these results.",
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
                    gap="md",
                ),
            ],
            size="xl",
        ),

        dmc.Modal(
            title="Data Sources & Technical Specifications",
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
                                                    "Part D Prescription Drug Event (PDE) data from the Centers for Medicare & Medicaid Services (CMS). National Drug Codes (NDCs) are linked to commercially available databases and aggregated across all strengths, dosage forms, and routes of administration.",
                                                    size="sm",
                                                ),
                                                dmc.Anchor(
                                                    "CMS Part D Drug Spending Dashboard →",
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
                                                dmc.Text("Data Processing Methodology", fw="bold", className="brooklyn-accent"),
                                                dmc.List(
                                                    [
                                                        dmc.ListItem("Weighted average calculations by claims volume"),
                                                        dmc.ListItem("Exclusion of drugs with fewer than 11 claims"),
                                                        dmc.ListItem("5-year historical trend preservation with redaction safeguards"),
                                                        dmc.ListItem("Compound Annual Growth Rate (CAGR) calculations"),
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
                        dmc.Stack(
                            [
                                dmc.Text("Key Metrics Definitions", fw="bold", className="brooklyn-brand"),
                                dmc.Grid(
                                    [
                                        dmc.GridCol(
                                            [
                                                dmc.List(
                                                    [
                                                        dmc.ListItem([
                                                            dmc.Text("Average Spending per Dosage Unit:", fw="bold", size="sm", span=True),
                                                            " Part D drug spending divided by dosage units, weighted by claims proportion"
                                                        ]),
                                                        dmc.ListItem([
                                                            dmc.Text("Total Spending:", fw="bold", size="sm", span=True),
                                                            " Aggregate drug spending for the Part D program during the benefit year"
                                                        ]),
                                                        dmc.ListItem([
                                                            dmc.Text("Average Spending per Beneficiary:", fw="bold", size="sm", span=True),
                                                            " Total Part D drug spending divided by unique beneficiaries utilizing the drug"
                                                        ]),
                                                    ],
                                                    size="sm",
                                                ),
                                            ],
                                            span=12,
                                        ),
                                    ],
                                    gutter="md",
                                ),
                            ],
                            gap="sm",
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