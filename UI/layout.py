import dash_mantine_components as dmc

from grid.ag_grid_definition import create_grid_component
from .header import header
from .navigation import navigation
from .modal import ModalContent
from .chart import ChartComponent
from .grid_component import GridComponent
from dash import dcc
from .footer import footer
from .select import create_filters

def layout():
     
    return dmc.Container(
    [
       header(),
       navigation(),
        ModalContent.about_modal_content(),
        ModalContent.how_to_use_modal_content(),
        ModalContent.key_insights_modal_content(),
        ModalContent.data_sources_modal_content(),
        create_filters(),
        

        # Chart Section - Professional Header
        ChartComponent.create_chart_header(),

        # Chart Container
        ChartComponent.create_chart_container(),
        
        # Data Table Section - Professional Header with Download
        GridComponent.create_grid_header(),
        
        # AG Grid Component
        GridComponent.create_grid_container(create_grid_component()),
        
        # Download Component
        dcc.Download(id="download-csv"),

        footer(),
        # Clean Footer
    ],
    size="xl",
    px="md",
    py="lg",
)