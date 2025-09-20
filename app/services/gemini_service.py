# In app/services/gemini_service.py

import os
import google.generativeai as genai
import pandas as pd

def analyze_with_gemini(company_data: list):
    """Sends price trend data to Gemini for speculative analysis."""
    if not company_data:
        return "Not enough data for analysis. Please check the company list."

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    df = pd.DataFrame(company_data)

    prompt = f"""
    Analyze the following stock data, which contains the current share price and the share price from one week ago for several companies.

    IMPORTANT: You are an AI assistant providing a speculative analysis based on very limited data. DO NOT give financial advice. Begin your response with the disclaimer: "This is a speculative analysis based on a one-week trend and is NOT financial advice. Past performance is not indicative of future results."

    For each company, perform the following:
    1. Calculate the percentage change over the last week.
    2. Based ONLY on this one-week momentum (positive or negative), provide a brief, speculative outlook on its potential short-term trajectory.
    3. Conclude by identifying which company shows the strongest positive momentum from this limited dataset.

    Data:
    {df.to_string()}
    """
    
    response = model.generate_content(prompt)
    return response.text