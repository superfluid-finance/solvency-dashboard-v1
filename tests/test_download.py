import datetime
import time
import json

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from src.data_extraction import run_query, data_processing

# CONFIG
# init transport client
transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/superfluid-finance/protocol-v1-matic")
client = Client(transport=transport)

# USER INPUT
# Get daterange in UNIX format  
timestamp_lt = datetime.datetime.now()
timestamp_gt = timestamp_lt - datetime.timedelta(days = 1)

# convert to unix timestamp
timestamp_lt = int(time.mktime(timestamp_lt.timetuple()))
timestamp_gt = int(time.mktime(timestamp_gt.timetuple()))

liquidation_events, account_token_snapshots = run_query(
    client=client,
    timestamp_lt=timestamp_lt,
    timestamp_gt=timestamp_gt
    )

with open("data/account_token_snapshots.json", "w") as file:

    file.write(json.dumps(account_token_snapshots))

    
with open("data/liquidation_events.json", "w") as file:

    file.write(json.dumps(liquidation_events))