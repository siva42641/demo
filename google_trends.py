from pytrends.request import TrendReq
import pandas as pd

def get_google_trends(geo_code='US', num_topics=10):
    """
    Fetches the top daily trending topics from Google Trends for a specified region.

    Args:
        geo_code (str): Two-letter country code (e.g., 'US', 'GB', 'IN').
        num_topics (int): The number of top topics to retrieve.

    Returns:
        pd.DataFrame: A DataFrame containing the trending topics.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        daily_trends = pytrends.trending_searches(pn=geo_code)

        if not daily_trends.empty:
            # Extract and clean the list of topics
            trends_list = []
            for index, row in daily_trends.head(num_topics).iterrows():
                if 'title' in row[0]:
                    title = row[0]['title'].strip()
                    explore_link = f"https://trends.google.com/trends/trendingsearches/daily?pn={geo_code}"
                    trends_list.append({'Title': title, 'Source': 'Google Trends', 'Link': explore_link})
                else:
                    # Handle case where the list is a single string or other format
                    for item in row[0]:
                        if isinstance(item, dict) and 'title' in item:
                            title = item['title'].strip()
                            explore_link = f"https://trends.google.com/trends/trendingsearches/daily?pn={geo_code}"
                            trends_list.append({'Title': title, 'Source': 'Google Trends', 'Link': explore_link})
            
            return pd.DataFrame(trends_list)
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"Error fetching Google Trends: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    trends_df = get_google_trends()
    if not trends_df.empty:
        print("Latest trending topics from Google Trends:")
        print(trends_df)
    else:
        print("Failed to fetch Google Trends data.")
