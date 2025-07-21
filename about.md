# Medicare Part D Drug Spending Dashboard

This dashboard is a professional, interactive web application for exploring and visualizing Medicare Part D drug spending data from CMS. It is inspired by the design and user experience of 46brooklyn.com, with a focus on clarity, accessibility, and modern data visualization best practices.

## Features
- Comprehensive filter system: Multi-select dropdowns for Product Name, Generic Name, Manufacturer, and Brand/Generic type
- Year range slider and Specialty Drug segmented control for advanced filtering
- Interactive AG Grid table for filtering, sorting, and exploring drug-level data
- Dynamic Plotly chart for visualizing gross spending and spending per claim over time
- Responsive, mobile-friendly layout using Dash Mantine Components
- 46Brooklyn-inspired color palette and card-based UI
- Data sourced from [CMS Medicare Part D Drug Spending Dashboard](https://data.cms.gov/tools/medicare-part-d-drug-spending-dashboard)

## Usage
- Use the filter panel to select multiple values for Product Name, Generic Name, Manufacturer, and Brand/Generic type
- Filter by year range and specialty drug status for targeted analysis
- The table and chart update automatically to reflect current filter selections
- Export chart images and download filtered data as CSV for presentations or reports

## Tech Stack
- Python, Dash, Plotly, Polars (for high-performance filtering), Dash Mantine Components, Dash AG Grid

## Credits
- Design inspired by [46brooklyn.com](https://www.46brooklyn.com/)
- Data from [CMS](https://data.cms.gov/tools/medicare-part-d-drug-spending-dashboard)
- Filtering architecture based on best practices from the Plotly/Polars Dash blog

---

For more information, see the code and documentation in this repository.
