import datetime
import time
import streamlit as st


def calculate_time_inputs(date_type, from_dt=None, to_dt=None):

    if date_type == "Last 5 Days":

        # USER INPUT
        # Get daterange in UNIX format  
        current_timestamp = datetime.datetime.now()
        year = current_timestamp.year
        month = current_timestamp.month
        day = current_timestamp.day
        hour = current_timestamp.hour

        if current_timestamp.minute >= 30:
            minute = 30
        else:
            minute = 0

        timestamp_lt = datetime.datetime(year, month, day, hour, minute, 0)
        timestamp_gt = timestamp_lt - datetime.timedelta(days = 5)

        # convert to unix timestamp
        timestamp_lt = int(time.mktime(timestamp_lt.timetuple()))
        timestamp_gt = int(time.mktime(timestamp_gt.timetuple()))

        return timestamp_lt, timestamp_gt

    if date_type == "Last 2 Weeks":

        # USER INPUT
        # Get daterange in UNIX format  
        current_timestamp = datetime.datetime.now()
        year = current_timestamp.year
        month = current_timestamp.month
        day = current_timestamp.day
        hour = current_timestamp.hour

        if current_timestamp.minute >= 30:
            minute = 30
        else:
            minute = 0

        timestamp_lt = datetime.datetime(year, month, day, hour, minute, 0)
        timestamp_gt = timestamp_lt - datetime.timedelta(days = 14)

        # convert to unix timestamp
        timestamp_lt = int(time.mktime(timestamp_lt.timetuple()))
        timestamp_gt = int(time.mktime(timestamp_gt.timetuple()))

        return timestamp_lt, timestamp_gt
    
    if date_type == "Custom Date Range":

        # USER INPUT
        # Get daterange in UNIX format  
        timestamp_lt = datetime.datetime.combine((to_dt + datetime.timedelta(days = 1)), datetime.time(0,0,0))
        timestamp_gt = datetime.datetime.combine(from_dt, datetime.time(0,0,0))

        # convert to unix timestamp
        timestamp_lt = int(time.mktime(timestamp_lt.timetuple()))
        timestamp_gt = int(time.mktime(timestamp_gt.timetuple()))

        return timestamp_lt, timestamp_gt
