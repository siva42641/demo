import os
import datetime
import feedparser
import requests
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
# CONFIG
FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://www.theverge.com/rss/index.xml"
]
SUMMARY_SENTENCES = 5
WP_URL = "https://siva42641.wpcomstaging.com/wp-json/wp/v2/posts"
WP_USER = os.environ.get("WP_USER")        # set in GitHub secrets
WP_PASS = os.environ.get("WP_PASS")        # set in GitHub secrets (application password)
def fetch_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None
def summarize_text(text, sentences=SUMMARY_SENTENCES):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences)
    return " ".join(str(s) for s in summary)
def generate_post(title, summary, original_url):
    return f"""
<h2>{title}</h2>
<p>{summary}</p>
<hr>
<p>:link: <a href="{original_url}">Read the full article here</a></p>
<p><em>This is an auto-generated summary post.</em></p>
"""
def publish_to_wordpress(title, content, tags=[]):
    headers = {"Content-Type": "application/json"}
    data = {
        "title": title,
        "content": content,
        "status": "publish",   # or "draft" if you want to review before publishing
        "tags": tags           # must match WordPress tag IDs
    }
    resp = requests.post(WP_URL, json=data, auth=(WP_USER, WP_PASS))
    if resp.status_code == 201:
        print(":white_tick: Post published:", resp.json().get("link"))
    else:
        print(":x: Failed:", resp.status_code, resp.text)
def main():
    for feed in FEEDS:
        d = feedparser.parse(feed)
        for entry in d.entries[:2]:
            url = entry.link
            title, text = fetch_article_text(url)
            if not text:
                continue
            summary = summarize_text(text)
            post_body = generate_post(title, summary, url)
            publish_to_wordpress(title, post_body)
if __name__ == "__main__":
    main()
