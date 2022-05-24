import pandas as pd

def data_processing(liquidation_events, account_token_snapshots):

    # DATA IMPORT
    agreementLiquidatedByEvents = pd.DataFrame(liquidation_events)
    accountTokenSnapshots = pd.DataFrame(account_token_snapshots)

    # TYPE FORMATTING
    accountTokenSnapshots["balanceUntilUpdatedAt"] = accountTokenSnapshots["balanceUntilUpdatedAt_form"]
    accountTokenSnapshots["totalNetFlowRate"] = accountTokenSnapshots["totalNetFlowRate_form"]
    accountTokenSnapshots.drop("balanceUntilUpdatedAt_form", axis=1)
    accountTokenSnapshots.drop("totalNetFlowRate_form", axis=1)
    agreementLiquidatedByEvents["rewardAmount"] = agreementLiquidatedByEvents["rewardAmount_form"]
    agreementLiquidatedByEvents.drop("rewardAmount_form", axis=1)

    # DATA WRANGLING
    agreementLiquidatedByEvents["targetAccount-token"] = agreementLiquidatedByEvents['targetAccount'] + " - " + agreementLiquidatedByEvents['token']
    agreementLiquidatedByEvents = agreementLiquidatedByEvents[[not elem for elem in agreementLiquidatedByEvents.duplicated(subset="targetAccount-token")]].reset_index()
    accountTokenSnapshots = accountTokenSnapshots[[not elem for elem in accountTokenSnapshots.duplicated(subset="id")]].reset_index()
    ## create index columns to merge datasets
    accountTokenSnapshots[['targetAccount', 'token']] = accountTokenSnapshots['id'].str.split('-', -1, expand=True)

    # merge datasets
    merged_data = agreementLiquidatedByEvents.merge(accountTokenSnapshots, how="left", on=["targetAccount", "token"])

    # select only relevant columns 
    merged_data = merged_data[["liquidatorAccount", "rewardAmount","timestamp", "balanceUntilUpdatedAt", "updatedAtTimestamp", "totalNetFlowRate"]]

    # rename columns 
    merged_data.rename(columns = {'timestamp':'liquidationTimestampUNIX', 'updatedAtTimestamp': 'dateCreatedTimestampUNIX', 'balanceUntilUpdatedAt': 'startingBalance'}, inplace = True)

    # calculations
    ## convert datatime column into unix format
    merged_data["liquidationTimestampUNIX"] = merged_data["liquidationTimestampUNIX"].astype(int).astype(str).str[:10].astype(int)

    merged_data["balanceSendAway"] = (merged_data["liquidationTimestampUNIX"] - merged_data["dateCreatedTimestampUNIX"].astype(int)) * merged_data["totalNetFlowRate"]
    merged_data["balanceAtLiquidation"] = merged_data["balanceSendAway"] + merged_data["startingBalance"]
    merged_data["responseTime_sec"] = merged_data["balanceAtLiquidation"] / merged_data["totalNetFlowRate"]

    # feature engineering
    merged_data["liquidationTimestampDatetime"] = pd.to_datetime(merged_data['liquidationTimestampUNIX'], unit='s')
    merged_data["date"] = merged_data["liquidationTimestampDatetime"].dt.date
    merged_data["hourOfDay"] = merged_data["liquidationTimestampDatetime"].dt.hour
    merged_data["dateHour"] = merged_data["liquidationTimestampDatetime"].dt.year.astype(str) + "-" + \
        merged_data["liquidationTimestampDatetime"].dt.month.astype(str).str.zfill(2) + "-" + \
        merged_data["liquidationTimestampDatetime"].dt.day.astype(str).str.zfill(2) + " " + \
        merged_data["liquidationTimestampDatetime"].dt.hour.astype(str).str.zfill(2) + ":00"


    return merged_data