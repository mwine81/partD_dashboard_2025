import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


class ModalContent:
    @staticmethod
    def about_modal_content():
        return dmc.Modal(
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
        )
    
    @staticmethod
    def how_to_use_modal_content():
        return dmc.Modal(
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
        )

    @staticmethod
    def key_insights_modal_content():
        return dmc.Modal(
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
        )

    @staticmethod
    def data_sources_modal_content():
        return dmc.Modal(
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
        )
