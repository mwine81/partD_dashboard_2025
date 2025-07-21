from helpers import load_data
import polars as pl
from polars import col as c
import polars.selectors as cs
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def aggregate_chart_data(data):
    """Aggregate data for chart visualization"""
    
    return (
        data
        .group_by('YEAR')
        .agg([
            c.Total_Spending.sum().alias('total_spending'),
            c.Total_Claims.sum().alias('total_claims')
        ])
        .with_columns(
            # spending per claim
            (c.total_spending / c.total_claims).alias('per_claim'),
            c.YEAR.alias('year')
        )
    )

def create_partd_figure(dataframe):
    """
    Create a professional Part D spending dashboard chart inspired by 46brooklyn.com
    
    Args:
        dataframe: Polars DataFrame with columns 'year', 'total_spending', 'total_claims', 'per_claim'
    
    Returns:
        plotly.graph_objects.Figure: Interactive chart showing spending trends
    """
    # Sort by year for proper line plotting
    
    df_sorted = dataframe.sort('year')
    
    # Determine the best scale for gross spending
    max_spending = df_sorted['total_spending'].max()
    if max_spending >= 1e9:
        spending_scale = 1e9
        spending_unit = "B"
        spending_label = "Gross Spending (Billions $)"
    elif max_spending >= 1e6:
        spending_scale = 1e6
        spending_unit = "M"
        spending_label = "Gross Spending (Millions $)"
    elif max_spending >= 1e3:
        spending_scale = 1e3
        spending_unit = "K"
        spending_label = "Gross Spending (Thousands $)"
    else:
        spending_scale = 1
        spending_unit = ""
        spending_label = "Gross Spending ($)"
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
        subplot_titles=("Medicare Part D Drug Spending Trends",)
    )
    
    # Add gross spending (total_spending) as bars
    fig.add_trace(
        go.Bar(
            x=df_sorted['year'].to_list(),
            y=(df_sorted['total_spending'] / spending_scale).to_list(),
            name="Gross Spending",
            marker_color='#1a365d',
            opacity=0.8,
            hovertemplate="<b>Year:</b> %{x}<br>" +
                         f"<b>Gross Spending:</b> $%{{y:.1f}}{spending_unit}<br>" +
                         "<extra></extra>"
        ),
        secondary_y=False,
    )
    
    # Add spending per claim as line
    fig.add_trace(
        go.Scatter(
            x=df_sorted['year'].to_list(),
            y=df_sorted['per_claim'].to_list(),
            mode='lines+markers',
            name="Spending per Claim",
            line=dict(color='#ed8936', width=3),
            marker=dict(size=8, color='#ed8936'),
            hovertemplate="<b>Year:</b> %{x}<br>" +
                         "<b>Spending per Claim:</b> $%{y:.2f}<br>" +
                         "<extra></extra>"
        ),
        secondary_y=True,
    )
    
    # Update x-axis
    fig.update_xaxes(
        title_text="Year",
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        title_font=dict(size=14, color='#2c3e50'),
        tickfont=dict(size=12, color='#2c3e50'),
        dtick=1  # Show only whole year values
    )
    
    # Update primary y-axis (gross spending)
    fig.update_yaxes(
        title_text=spending_label,
        secondary_y=False,
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        title_font=dict(size=14, color='#1a365d'),
        tickfont=dict(size=12, color='#1a365d'),
        tickformat='$.1f'
    )
    
    # Update secondary y-axis (spending per claim)
    fig.update_yaxes(
        title_text="Average Spending per Claim ($)",
        secondary_y=True,
        title_font=dict(size=14, color='#ed8936'),
        tickfont=dict(size=12, color='#ed8936'),
        tickformat='$.2f'
    )
    
    # Update layout for professional 46Brooklyn appearance
    fig.update_layout(
        title=dict(
            text="Medicare Part D Drug Spending Trends (2013-2023)",
            x=0.5,
            font=dict(size=20, color='#1a365d', family='Source Sans Pro, Arial, sans-serif', weight='bold')
        ),
        plot_bgcolor='white',
        paper_bgcolor='#f8fafc',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.8,
            font=dict(size=12, color='#1a365d', family='Source Sans Pro, Arial, sans-serif'),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e2e8f0",
            borderwidth=1
        ),
        margin=dict(l=80, r=80, t=100, b=80),
        height=600,
        hovermode='x unified',
        font=dict(family='Inter, Arial, sans-serif'),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='#e2e8f0',
            mirror=True
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='#e2e8f0',
            mirror=True
        ),
        yaxis2=dict(
            showline=True,
            linewidth=1,
            linecolor='#e2e8f0',
            mirror=True
        )
    )
    
    # Add professional data source annotation
    fig.add_annotation(
        text="Data Source: CMS Medicare Part D Drug Spending Dashboard",
        xref="paper", yref="paper",
        x=1, y=-0.12,
        xanchor='right', yanchor='top',
        font=dict(size=10, color='#718096', family='Inter, Arial, sans-serif'),
        showarrow=False
    )
    
    return fig

if __name__ == "__main__":
    pass
    # This will display the figure in a web browser