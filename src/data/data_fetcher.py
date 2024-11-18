import yfinance as yf

def get_security_closing_price(ticker: str, date: str):
    """
    Returns the closing price for the input ticker and date.

    Date must be in the format of YYYY-MM-DD.
    """
    security = yf.Ticker(ticker)

    # TODO: Check if this works, we might need to set date to the date before(it might be [start, end) and also make sure that it's giving it for the right date)
    # Fetch historical data for the given date range (same start and end date)
    historical_data = security.history(start=date, end=date)
    
    # Check if the data exists for the specified date
    if not historical_data.empty:
        return historical_data['Close'].iloc[0]
    else:
        print(f"No data available for {ticker} on {date}")
        return None

# TODO: Implement a method to get current options prices    
