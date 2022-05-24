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

        if len(response["agreementLiquidatedV2Events"]) != first_n:
            
            break

        skip_n += first_n

    account_token_snapshots = []

    #for liquidation_event in stqdm(liquidation_events, desc="Querying accountTokenSnapshots..."):
    for liquidation_event in liquidation_events:

        Id = f"{liquidation_event['targetAccount']}-{liquidation_event['token']}"
        BlockNumber = int(liquidation_event["blockNumber"]) - 1 

        ## Get Account Token Snapshotssub
        # queries
        query = gql("""
            query AccountTokenSnapshot ($number: Int!, $id: ID!){
                accountTokenSnapshots(
                    block: {
                        number: $number
                        }, 
                    where: {
                        id: $id
                }) {
                id
                balanceUntilUpdatedAt
                updatedAtTimestamp
                totalNetFlowRate
                }
            }
        """)

        # Set query parameters
        params = {
            "id": Id,
            "number": BlockNumber,
        }

        response = client.execute(query, variable_values=params)

        account_token_snapshots = account_token_snapshots + response["accountTokenSnapshots"]
        
        # convert GWEI to ETH
        # for snapshot in account_token_snapshots:
        for event in liquidation_events:
            event["rewardAmount_form"] = float(event["rewardAmount"]) / (10**18) 
        
        for snapshot in account_token_snapshots:
            snapshot["balanceUntilUpdatedAt_form"] = float(snapshot["balanceUntilUpdatedAt"]) / (10**18)
            snapshot["totalNetFlowRate_form"] =  float(snapshot["totalNetFlowRate"]) / (10**18)

    return liquidation_events, account_token_snapshots
