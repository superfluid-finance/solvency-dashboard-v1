from gql import gql
import streamlit as st

@st.cache(show_spinner=False, suppress_st_warning=True)
def run_query(client, timestamp_gt, timestamp_lt):

    ## Get Agreement Liquidation Events
    # queries
    query = gql("""
        query agreementLiquidatedV2Events ($timestamp_lt: Int!, $timestamp_gt: Int!, $first: Int!, $skip: Int!) {
            agreementLiquidatedV2Events(where: { 
                timestamp_lt: $timestamp_lt,
                timestamp_gt: $timestamp_gt
                }
                first: $first,
                skip: $skip,
                orderBy: timestamp,
                orderDirection: desc
                ) {
            blockNumber
            id
            liquidatorAccount
            rewardAccount
            rewardAmount
            targetAccount
            timestamp
            token
            }
        }
    """)

    liquidation_events = []

    first_n = 1000
    skip_n = 0

    while True:

        first_n = 1000
        skip_n = 0

        # Set query parameters
        params = {
            "first": first_n,
            "skip": skip_n,
            "timestamp_lt": timestamp_lt,
            "timestamp_gt": timestamp_gt,
        }

        response = client.execute(query, variable_values=params)

        liquidation_events = liquidation_events + response["agreementLiquidatedV2Events"]

        timestamps = [int(response['timestamp']) for response in liquidation_events]
        min_time = min(timestamps) + 1

        if len(response["agreementLiquidatedV2Events"]) != first_n:
            
            break

        skip_n += first_n

        if skip_n > 5000:

            skip_n = 0
            startedAtTimestamp_lt = min_time

    max_block = max([int(elem["blockNumber"]) for elem in liquidation_events])
    min_block = min([int(elem["blockNumber"]) for elem in liquidation_events]) - 1
    
    ## Get Account Token Snapshotssub
    # queries
    query = gql("""
        query MyQuery($skip: Int!, $first: Int!, $blockNumber_gte: BigInt!, $blockNumber_lt: BigInt!) {
            accountTokenSnapshotLogs(
                skip: $skip
                orderBy: blockNumber
                orderDirection: desc
                first: $first
                where: {
                    blockNumber_gte: $blockNumber_gte, 
                    blockNumber_lt: $blockNumber_lt
                }
            ) {
                balance
                blockNumber
                id
                order
                timestamp
                totalDeposit
                totalNetFlowRate
                triggeredByEventName
            }
        }
    """)


    account_token_snapshots = []

    first_n = 1000
    skip_n = 0

    while True:

        # Set query parameters
        params = {
            "first": first_n,
            "skip": skip_n,
            "blockNumber_gte": min_block,
            "blockNumber_lt": max_block,
        }

        response = client.execute(query, variable_values=params)

        account_token_snapshots = account_token_snapshots + response["accountTokenSnapshotLogs"]

        blockstamps = [int(response['blockNumber']) for response in account_token_snapshots]
        min_block_new = min(blockstamps) + 1

        if len(response["accountTokenSnapshotLogs"]) != first_n:
            
            break

        skip_n += first_n

        if skip_n > 5000:

            skip_n = 0
            max_block = min_block_new
    
    # convert GWEI to ETH
    for event in liquidation_events:
        event["rewardAmount_form"] = float(event["rewardAmount"]) / (10**18) 
    
    for snapshot in account_token_snapshots:
        snapshot["balance_form"] = float(snapshot["balance"]) / (10**18)
        snapshot["totalNetFlowRate_form"] =  float(snapshot["totalNetFlowRate"]) / (10**18)

    return liquidation_events, account_token_snapshots
