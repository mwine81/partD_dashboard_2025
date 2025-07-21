import dash_mantine_components as dmc
from dash import html, get_asset_url
from dash_iconify import DashIconify

def header():
    # Header Section - Clean Minimalist Design
    return dmc.Paper(
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
        )