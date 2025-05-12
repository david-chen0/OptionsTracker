import sys
import os
from datetime import date, datetime, timedelta
import yfinance as yf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from util.common import *
from util.rate_limiter import *

# Tomorrow's date formatted as YYYY-MM-DD
tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

# Dictionary containing the tickers we've already instantiated(computing power for memory tradeoff)
tickers = {}

# Rate limiter for our calls to yfinance
rate_limiter = RateLimitedExecutor(100, 1.0) # 100 calls a second

def get_security_ticker_object(ticker: str) -> yf.Ticker:
    """
    Returns the Ticker object for the input ticker string

    TODO: Check if exception is thrown when the ticker doesn't exist
    """
    if ticker in tickers:
        return tickers[ticker]

    security = rate_limiter.call(yf.Ticker, ticker)
    tickers[ticker] = security
    return security

def get_security_closing_price(ticker: str, date: date) -> float:
    """
    Returns the closing price for the input ticker and date.

    Date must be in the format of YYYY-MM-DD.
    """
    security = get_security_ticker_object(ticker)

    # Fetches data from current day to next day since the results are [start date, end day)
    current_day = datetime.combine(date, datetime.min.time())
    next_day = current_day + timedelta(days=1)
    historical_data = rate_limiter.call(security.history, start=current_day, end=next_day)
    
    # Check if the data exists for the specified date
    if historical_data.empty:
        raise ValueError(f"No data available for {ticker} on {current_day}")
    
    # Rounding the result to the penny since Yahoo finance's result often has floating point errors
    return round(historical_data['Close'].iloc[0], 2)

def get_current_option_price(
    ticker: str,
    expiration_date: str,
    strike: float,
    is_call: bool
) -> float:
    """
    Returns the current price for the input option

    ticker: Ticker for the underlying security
    expiration_date: Expiration date of the option as a YYYY-MM-DD string
    strike: Strike price of the option
    is_call: True if option is a call option, false for put option
    """
    security = get_security_ticker_object(ticker)
    
    expiry = expiration_date.strftime("%Y-%m-%d")
    entire_option_chain = rate_limiter.call(security.option_chain, date=expiry)
    option_chain = entire_option_chain.calls if is_call else entire_option_chain.puts
    
    try:
        option = option_chain[option_chain.strike == strike]
        return float(option.lastPrice.iloc[0])
    except:
        # print(option_chain) # for debugging, remove once done
        raise Exception(f"Provided strike {strike} with expiration date {expiration_date} is not present in the option chain for {ticker}")
