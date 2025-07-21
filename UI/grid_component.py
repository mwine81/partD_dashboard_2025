import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc
import dash_ag_grid as dag
from grid.ag_grid_definition import columnDefs

class GridComponent:
    
    @staticmethod
    def create_grid_header():
        return dmc.Paper(
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
                                        dmc.Badge("Interactive Table", color="orange", variant="light"),
                                        dmc.Group([
                                            dmc.Button(
                                                [
                                                    DashIconify(icon="tabler:download", width=16),
                                                    "CSV"
                                                ],
                                                variant="light",
                                                color="gray",
                                                size="sm",
                                                id="download-button",
                                                style={"color": "white", "backgroundColor": "rgba(255,255,255,0.2)"},
                                            ),
                                            dmc.Tooltip(
                                                "Download current filtered data as CSV",
                                                label="CSV Export",
                                                position="bottom"
                                            )
                                        ], gap="xs")
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
        )
    
    @staticmethod
    def create_grid_container():
        """Create the AG Grid container with dynamic data"""
        return dmc.Paper([
            dcc.Loading(
                id="loading-grid",
                type="dot",
                color="#1a365d",
                children=[
                    dag.AgGrid(
                        id="ag-grid",
                        rowData=[],  # Will be populated by callback
                        columnDefs=columnDefs,
                        className="ag-theme-alpine",
                        style={"height": "600px"},
                        dashGridOptions={
                            "pagination": True,
                            "paginationPageSize": 20,
                            "domLayout": "normal",
                            "defaultColDef": {
                                "resizable": True,
                                "sortable": True,
                                "filter": True,
                            },
                            "enableRangeSelection": True,
                            "suppressExcelExport": False,
                            "rowSelection": "multiple",
                        }
                    )
                ]
            )
        ], className="brooklyn-card", style={"marginTop": 0, "paddingTop": 0})


