import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html, get_asset_url
from dash_iconify import DashIconify

def footer():
    return dmc.Paper(
        [
            dmc.Stack([
                # Main footer content
                dmc.Grid([
                    # Left section - About and attribution
                    dmc.GridCol([
                        dmc.Stack([
                            dmc.Group([
                                DashIconify(icon="tabler:info-circle", width=16, color="#1a365d"),
                                dmc.Text("Dashboard Information", fw="bold", size="sm", style={"color": "#1a365d"})
                            ], gap="xs"),
                            dmc.Text(
                                "Dashboard methodology inspired by 46brooklyn.com's approach to Medicare Part D data analysis. Built with modern data visualization techniques for comprehensive drug spending insights.",
                                size="xs",
                                c="gray",
                                lh=1.4
                            ),
                            dmc.Group([
                                dmc.Anchor(
                                    "CMS Data Source",
                                    href="https://data.cms.gov/tools/medicare-part-d-drug-spending-dashboard",
                                    target="_blank",
                                    size="xs",
                                    style={"color": "#1a365d"}
                                ),
                                dmc.Text("•", size="xs", c="gray"),
                                dmc.Anchor(
                                    "46brooklyn Research",
                                    href="https://www.46brooklyn.com/",
                                    target="_blank",
                                    size="xs",
                                    style={"color": "#1a365d"}
                                )
                            ], gap="xs")
                        ], gap="sm")
                    ], span=8),
                    
                    # Right section - 46brooklyn social media
                    dmc.GridCol([
                        dmc.Stack([
                            dmc.Group([
                                DashIconify(icon="tabler:share", width=16, color="#ed8936"),
                                dmc.Text("Follow 46brooklyn Research", fw="bold", size="sm", style={"color": "#ed8936"})
                            ], gap="xs"),
                            dmc.Text(
                                "Stay updated with the latest drug pricing research and insights:",
                                size="xs",
                                c="gray",
                                lh=1.4
                            ),
                            dmc.Group([
                                dmc.Tooltip(
                                    label="Follow @46brooklyndata on Twitter",
                                    children=[
                                        html.A(
                                            dmc.ActionIcon(
                                                DashIconify(icon="mdi:twitter", width=18),
                                                variant="subtle",
                                                color="blue",
                                                size="md",
                                                style={"transition": "all 0.2s ease"}
                                            ),
                                            href="https://twitter.com/46brooklyndata",
                                            target="_blank",
                                            style={"textDecoration": "none"}
                                        )
                                    ]
                                ),
                                dmc.Tooltip(
                                    label="Connect on LinkedIn",
                                    children=[
                                        html.A(
                                            dmc.ActionIcon(
                                                DashIconify(icon="mdi:linkedin", width=18),
                                                variant="subtle",
                                                color="blue",
                                                size="md",
                                                style={"transition": "all 0.2s ease"}
                                            ),
                                            href="https://www.linkedin.com/company/46brooklyn-research/",
                                            target="_blank",
                                            style={"textDecoration": "none"}
                                        )
                                    ]
                                ),
                                dmc.Tooltip(
                                    label="Follow on Instagram",
                                    children=[
                                        html.A(
                                            dmc.ActionIcon(
                                                DashIconify(icon="mdi:instagram", width=18),
                                                variant="subtle",
                                                color="pink",
                                                size="md",
                                                style={"transition": "all 0.2s ease"}
                                            ),
                                            href="https://www.instagram.com/46brooklynresearch/",
                                            target="_blank",
                                            style={"textDecoration": "none"}
                                        )
                                    ]
                                ),
                                dmc.Tooltip(
                                    label="Like on Facebook",
                                    children=[
                                        html.A(
                                            dmc.ActionIcon(
                                                DashIconify(icon="mdi:facebook", width=18),
                                                variant="subtle",
                                                color="blue",
                                                size="md",
                                                style={"transition": "all 0.2s ease"}
                                            ),
                                            href="https://www.facebook.com/46brooklyn/",
                                            target="_blank",
                                            style={"textDecoration": "none"}
                                        )
                                    ]
                                ),
                                dmc.Tooltip(
                                    label="Support their research",
                                    children=[
                                        html.A(
                                            dmc.ActionIcon(
                                                DashIconify(icon="tabler:heart-filled", width=18),
                                                variant="subtle",
                                                color="red",
                                                size="md",
                                                style={"transition": "all 0.2s ease"}
                                            ),
                                            href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YEF4YPTGZN9EJ&source=url",
                                            target="_blank",
                                            style={"textDecoration": "none"}
                                        )
                                    ]
                                )
                            ], gap="xs")
                        ], gap="sm")
                    ], span=4)
                ], gutter="lg"),
                
                # Bottom section - Copyright and additional info
                dmc.Divider(color="gray"),
                dmc.Group([
                    dmc.Group([
                        dmc.Text("© 2025 Medicare Part D Analytics Dashboard", size="xs", c="gray"),
                        dmc.Text("•", size="xs", c="gray"),
                        dmc.Text("Inspired by 46brooklyn Research methodology", size="xs", c="gray")
                    ], gap="xs"),
                    dmc.Group([
                        dmc.Badge(
                            [DashIconify(icon="tabler:database", width=12), "CMS Data"],
                            variant="dot",
                            color="blue",
                            size="xs"
                        ),
                        dmc.Badge(
                            [DashIconify(icon="tabler:chart-line", width=12), "Analytics"],
                            variant="dot",
                            color="green",
                            size="xs"
                        )
                    ], gap="xs")
                ], justify="space-between", wrap="wrap")
            ], gap="md")
        ],
        p="lg",
        radius="md",
        className="brooklyn-paper",
        mt="xl",
        style={
            "borderTop": "1px solid #e2e8f0",
            "backgroundColor": "#f8fafc"
        },
    )
 