import dash_ag_grid as dag
from helpers import load_data


columnDefs = [
    {"field": "product_name", "filter": True},
    {"field": "generic_name", "filter": True},
    {"field": "manufacturer", "filter": True},
    {"field": "total_spending", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"}, "filter": True},
    {"field": "total_dosage_units", "type": "rightAligned", "valueFormatter": {"function": "d3.format(',')(params.value)"}, "filter": True},
    {"field": "total_claims", "type": "rightAligned", "valueFormatter": {"function": "d3.format(',')(params.value)"}, "filter": True},
    {"field": "total_beneficiaries", "type": "rightAligned", "valueFormatter": {"function": "d3.format(',')(params.value)"}, "filter": True},
    {"field": "calc_average_spending_per_dosage_unit", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"}, "filter": True},
    {"field": "calc_average_spending_per_claim", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"}, "filter": True},
    {"field": "calc_average_spending_per_beneficiary", "type": "rightAligned", "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"}, "filter": True},
    {"field": "outlier_flag", "filter": True},
    {"field": "year", "filter": True},
    {"field": "brand_vs_generic", "filter": True},
    {"field": "specialty_drug", "filter": True},
]


component = dag.AgGrid(
    id="ag-grid",
    rowData=load_data().collect().to_dicts(),
    columnDefs=columnDefs,
)



