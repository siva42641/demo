from pytrends.request import TrendReq
import pandas as pd

def get_google_daily_trends(country_code='US'):
    """
    Fetches the daily trending searches from Google for a specific country.
    
    Args:
        country_code (str): The two-letter country code (e.g., 'US', 'IN', 'GB').
        
    Returns:
        pd.DataFrame: A DataFrame containing the trending searches, or None on failure.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        daily_trends_df = pytrends.trending_searches(pn=country_code)
        return daily_trends_df
    except Exception as e:
        print(f"Error fetching Google daily trends: {e}")
        return None

if __name__ == "__main__":
    # Fetch trends for the United States
    trends = get_google_daily_trends(country_code='US')
    
    if trends is not None:
        print("Latest Google Daily Trends (US):")
        if not trends.empty:
            # The '0' column contains the trending searches
            for index, row in trends.iterrows():
                print(f"- {row[0]}")
        else:
            print("No trends available.")
