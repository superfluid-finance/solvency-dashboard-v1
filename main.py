import datetime
import streamlit as st

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from src.data_extraction import run_query
from src.data_manipulation import data_processing
from src.data_visualization import timeline_plot
from src.utils import calculate_time_inputs

# CONFIG
# init transport client
transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/superfluid-finance/protocol-v1-matic")
client = Client(transport=transport)

# INPUTS
with st.sidebar:
    
    st.subheader("Fetch Data")

    with st.form(key="my_form"):

        date_type = st.radio("", options=["Last 5 Days", "Last 2 Weeks", "Custom Date Range"])
        
        from_dt = st.date_input("Date From", value=(datetime.datetime.now() - datetime.timedelta(days = 5)))

        to_dt = st.date_input("Date To", value=datetime.datetime.now())

        st.form_submit_button("Re-Run")


timestamp_lt, timestamp_gt = calculate_time_inputs(
    date_type=date_type, 
    from_dt=from_dt, 
    to_dt=to_dt
)

# DATA DOWNLOAD
with st.spinner('Querying Subgraph...'):

    liquidation_events, account_token_snapshots = run_query(
        client=client,
        timestamp_lt=timestamp_lt,
        timestamp_gt=timestamp_gt
    )

with st.spinner('Processing Subgraph Data...'):

    liquidation_events_data = data_processing(
        liquidation_events=liquidation_events, 
        account_token_snapshots=account_token_snapshots
    )

st.title('Solvency Response Dashboard')

#st.dataframe(liquidation_events_data)

fig = timeline_plot(liquidation_events_data)

st.plotly_chart(fig)

st.write(st.session_state)
