# In app/routes.py

from flask import Blueprint, jsonify, render_template
from .services import data_fetcher, analyzer, gemini_service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@main_bp.route('/api/analyze/<city>', methods=['GET'])
def analyze_city(city):
    """API endpoint to analyze companies in a given city."""
    print(f"\nReceived request for city: {city}")
    companies = data_fetcher.get_tickers_by_city(city)
    if not companies:
        return jsonify({"error": "City not found"}), 404
        
    results = []
    for name, ticker in companies.items():
        print(f"Fetching price data for {name} ({ticker})...")
        price_data = data_fetcher.get_price_data(ticker)
        
        if price_data:
            print(f"  -> Success for {ticker}.")
            results.append({
                'Company': name,
                'Ticker': ticker,
                'Current Price': price_data['current_price'],
                'Price Last Week': price_data['week_ago_price']
            })
        else:
            print(f"  -> Failed to fetch price data for {ticker}.")

    analysis = gemini_service.analyze_with_gemini(results)
    return jsonify({"analysis": analysis})

# This endpoint is no longer needed as we simplified the sidebar
# to avoid API call issues on page load.