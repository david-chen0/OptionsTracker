import sys
import os
from datetime import datetime, timedelta
import yfinance as yf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from util.common import *

# Tomorrow's date formatted as YYYY-MM-DD
tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

async def get_security_closing_price(ticker: str, date: str) -> float:
    """
    Returns the closing price for the input ticker and date.

    Date must be in the format of YYYY-MM-DD.
    """
    security = yf.Ticker(ticker)

    # Fetches data from current day to next day since the results are [start date, end day)
    historical_data = security.history(start=date, end=get_next_day(date))
    
    # Check if the data exists for the specified date
    if historical_data.empty:
        raise ValueError(f"No data available for {ticker} on {date}")
    
    # Rounding the result to the penny since Yahoo finance's result often has floating point errors
    return round(historical_data['Close'].iloc[0], 2)

# TODO: Implement a method to get current options prices    
