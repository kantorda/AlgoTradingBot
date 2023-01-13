###
# Implementation of the trading algorithm
###

import AlpacaAPI
from datetime import date, datetime, timedelta
import numpy as np

days = 7
percent_variance = 0.2


def get_start_date(days):
    today = date.today()
    start = today

    count = 0
    while count < days:
        start = start - timedelta(days=1)

        # get list of all days
        today_str = str(today)
        start_str = str(start)

        count = abs(np.busday_count(today_str, start_str))

    start_dt = datetime.combine(start, datetime.min.time())
    return start_dt


def calculate_sma(bars, symbol):
    sum = 0

    for day in bars[symbol]:
        sum = sum + day.close

    sma = sum / len(bars[symbol])

    return sma


def should_buy(symbol):
    try:
        start_date = get_start_date(days)
        bars = AlpacaAPI.get_bar_data(symbol, start_date)

        sma = calculate_sma(bars, symbol)
        latest_quote = AlpacaAPI.get_latest_quote(symbol)

        if latest_quote <= sma:
            return False

        if sma * (1 + percent_variance) <= latest_quote:
            return True

        return False
    except:
        return False
