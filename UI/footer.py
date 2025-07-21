import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html, get_asset_url

def footer():
    return dmc.Paper(
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
        )
 