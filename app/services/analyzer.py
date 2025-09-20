def calculate_yoy_margin_change(income_data):
    """Calculates the Year-over-Year change in Net Profit Margin."""
    try:
        current_margin = income_data[0]['netIncome'] / income_data[0]['revenue']
        previous_margin = income_data[1]['netIncome'] / income_data[1]['revenue']
        
        if previous_margin == 0: return float('inf')
        
        yoy_change = ((current_margin - previous_margin) / abs(previous_margin)) * 100
        return yoy_change
    except (KeyError, ZeroDivisionError, TypeError, IndexError):
        return None