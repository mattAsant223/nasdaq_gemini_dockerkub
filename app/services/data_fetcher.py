import os
import requests
import time
from datetime import datetime, timedelta

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

# --- Company Lists (No Change) ---
AUSTIN_COMPANIES = { "Tesla, Inc.": "TSLA", "Oracle Corporation": "ORCL", "Dell Technologies Inc.": "DELL", "YETI Holdings, Inc.": "YETI", "SolarWinds Corporation": "SWI" }
DALLAS_COMPANIES = { "AT&T Inc.": "T", "Texas Instruments Incorporated": "TXN", "Southwest Airlines Co.": "LUV", "Jacobs Solutions Inc.": "J", "Builders FirstSource, Inc.": "BLDR" }

def get_tickers_by_city(city: str):
    if city.lower() == 'austin': return AUSTIN_COMPANIES
    elif city.lower() == 'dallas': return DALLAS_COMPANIES
    return {}

# --- Updated Function to Get Price Data ---

def get_price_data(ticker: str):
    """Fetches most recent and previous week's closing prices for a stock."""
    params = {
        "function": "TIME_SERIES_WEEKLY", # Switched to weekly endpoint
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # The key is now 'Weekly Time Series'
        time_series = data.get("Weekly Time Series")
        
        # Enhanced error printing
        if not time_series or len(time_series) < 2:
            print(f"--> ERROR for {ticker}: Could not retrieve sufficient weekly data.")
            print(f"--> API Response: {data}") # Prints the full error response from the API
            return None

        # Simplified logic for weekly data
        sorted_dates = sorted(time_series.keys(), reverse=True)
        
        latest_week_date = sorted_dates[0]
        previous_week_date = sorted_dates[1]

        latest_price = float(time_series[latest_week_date]['4. close'])
        previous_week_price = float(time_series[previous_week_date]['4. close'])

        time.sleep(1) # Continue to respect API rate limits
        return {"current_price": latest_price, "week_ago_price": previous_week_price}

    except requests.exceptions.HTTPError as http_err:
        print(f"--> HTTP ERROR for {ticker}: {http_err}")
        print(f"--> Response Body: {response.text}")
        return None
    except Exception as e:
        print(f"--> An unexpected error occurred for {ticker}: {e}")
        return None