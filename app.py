import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import feedparser
from flask import Flask, render_template

app = Flask(__name__)

def fetch_news_rss():
    feed_url = 'https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines'
    feed = feedparser.parse(feed_url)
    news_headlines = [entry.title for entry in feed.entries]
    return news_headlines

def fetch_news_web():
    url = 'https://www.bloomberg.com/markets/stocks'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h1')
    news_headlines = [headline.text.strip() for headline in headlines]
    return news_headlines

def analyze_sentiment(headlines):
    polarity_scores = []
    detailed_analysis = []

    for headline in headlines:
        analysis = TextBlob(headline)
        polarity = analysis.sentiment.polarity
        polarity_scores.append(polarity)
        detailed_analysis.append({'headline': headline, 'polarity': polarity})

    avg_polarity = sum(polarity_scores) / len(polarity_scores) if polarity_scores else 0
    return avg_polarity, detailed_analysis

def get_market_opinion():
    rss_headlines = fetch_news_rss()
    web_headlines = fetch_news_web()
    all_headlines = rss_headlines + web_headlines
    avg_sentiment, detailed_analysis = analyze_sentiment(all_headlines)

    return all_headlines, detailed_analysis, avg_sentiment

@app.route('/')
def index():
    all_headlines, detailed_analysis, avg_sentiment = get_market_opinion()

    overall_sentiment = "neutral"
    if avg_sentiment > 0.1:
        overall_sentiment = "positive"
    elif avg_sentiment < -0.1:
        overall_sentiment = "negative"

    return render_template('index.html', headlines=all_headlines, analysis=detailed_analysis, opinion=overall_sentiment)

if __name__ == '__main__':
    app.run(debug=True)
