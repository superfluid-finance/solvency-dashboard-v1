import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

def timeline_plot(merged_data):

    # Plot 2
    # set to ignore deprecation warning messages on notebook
    warnings.filterwarnings('ignore')

    # data wrangling
    date_hour_data = merged_data.groupby("dateHour")["responseTime_sec"].mean().reset_index()
    date_hour_data["n"] = merged_data.groupby("dateHour")["responseTime_sec"].count().reset_index()["responseTime_sec"]

    fig = make_subplots(
        rows=2, 
        cols=1,
        subplot_titles=('Hourly Response time over time', 'Number of Liquidation Events')
        )

    fig.append_trace(go.Line(
        x=date_hour_data["dateHour"],
        y=date_hour_data["responseTime_sec"],
        line=dict(color='rgb(16,187,52)') 
    ), row=1, col=1)

    fig.append_trace(go.Line(
        x=date_hour_data["dateHour"],
        y=date_hour_data["n"],
        line=dict(
            color='rgb(16,187,52)',
            dash='dash'
        ) 
    ), row=2, col=1)

    fig.update_layout(
        title_text="Timeseries Data",
    )
    
    return fig