from pytrends.request import TrendReq
import requests, time, json, os, datetime as dt

os.makedirs("data", exist_ok=True)
pytrends = TrendReq(hl='en-US', tz=330)

def google_trends(seed):
    pytrends.build_payload([seed], timeframe='now 7-d', geo='IN')
    related = pytrends.related_queries()
    rising = related.get(seed, {}).get('rising', [])
    return [r['query'] for r in (rising.to_dict('records') if hasattr(rising,'to_dict') else [])]

def stackexchange(tag):
    url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=votes&tagged={tag}&site=stackoverflow&pagesize=20"
    return [i['title'] for i in requests.get(url, timeout=20).json().get('items',[])]

def main():
    seeds = open("data/seed_keywords.txt").read().splitlines()
    ideas = {}
    for s in seeds:
        ideas[s] = {
            "trends": google_trends(s)[:10],
            "stack": stackexchange(s.split()[0])[:10]
        }
        time.sleep(1)
    stamp = dt.datetime.utcnow().strftime("%Y%m%d%H%M")
    with open(f"data/ideas_{stamp}.json","w") as f: json.dump(ideas,f,indent=2)
if __name__ == "__main__":
    main()
