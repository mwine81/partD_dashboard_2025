import dash_ag_grid as dag
from helpers import load_data


# Column definitions with proper naming and formatting
columnDefs = [
    {"field": "Product_Name", "headerName": "Product Name", "filter": True, "minWidth": 200},
    {"field": "Generic_Name", "headerName": "Generic Name", "filter": True, "minWidth": 180},
    {"field": "Manufacturer", "headerName": "Manufacturer", "filter": True, "minWidth": 150},
    {"field": "Total_Spending", "headerName": "Total Spending", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.0f')(params.value)"}, "filter": True, "minWidth": 130},
    {"field": "Total_Dosage_Units", "headerName": "Dosage Units", "type": "rightAligned", "valueFormatter": {"function": "d3.format(',')(params.value)"}, "filter": True, "minWidth": 120},
    {"field": "Total_Claims", "headerName": "Total Claims", "type": "rightAligned", "valueFormatter": {"function": "d3.format(',')(params.value)"}, "filter": True, "minWidth": 120},
    {"field": "Total_Beneficiaries", "headerName": "Beneficiaries", "type": "rightAligned", "valueFormatter": {"function": "d3.format(',')(params.value)"}, "filter": True, "minWidth": 120},
    {"field": "Calc_Average_Spending_Per_Dosage_Unit", "headerName": "$/Unit", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"}, "filter": True, "minWidth": 100},
    {"field": "Calc_Average_Spending_Per_Claim", "headerName": "$/Claim", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"}, "filter": True, "minWidth": 100},
    {"field": "Calc_Average_Spending_Per_Beneficiary", "headerName": "$/Beneficiary", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.0f')(params.value)"}, "filter": True, "minWidth": 130},
    {"field": "Outlier_Flag", "headerName": "Outlier", "filter": True, "minWidth": 80},
    {"field": "YEAR", "headerName": "Year", "filter": True, "minWidth": 80},
    {"field": "Brand_vs_Generic", "headerName": "Type", "filter": True, "minWidth": 100},
    {"field": "SPECIALTY_DRUG", "headerName": "Specialty", "filter": True, "minWidth": 100},
]

# AG Grid component with professional styling
component = dag.AgGrid(
    id="ag-grid",
    rowData=load_data().collect().to_dicts(),
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



