import dash_mantine_components as dmc
from dash import html, get_asset_url
from dash_iconify import DashIconify

def navigation():
    return dmc.Paper(
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
    )

