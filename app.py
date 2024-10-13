from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import feedparser

app = Flask(__name__)

def fetch_news_rss():
    # Fetch RSS feed from MarketWatch
    feed_url = 'https://cointelegraph.com/rss/category/market-analysis'
    feed = feedparser.parse(feed_url)
    news_headlines = []

    # Extract headlines from RSS feed
    for entry in feed.entries:
        news_headlines.append(entry.title)
    
    return news_headlines

def fetch_news_web(url):
    # Web scrape headlines from the provided URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find headline elements (assumed to be <h1> for demonstration; update as needed)
    headlines = soup.find_all('h1')

    news_headlines = [headline.text.strip() for headline in headlines]
    return news_headlines

def analyze_sentiment(headlines):
    polarity_scores = []
    detailed_analysis = []
    
    # Analyze sentiment of each headline
    for headline in headlines:
        analysis = TextBlob(headline)
        polarity = analysis.sentiment.polarity  # -1 to +1 (negative to positive)
        polarity_scores.append(polarity)
        # Append detailed analysis for each headline
        detailed_analysis.append({
            'headline': headline,
            'polarity': polarity
        })
    
    # Calculate average sentiment
    avg_polarity = sum(polarity_scores) / len(polarity_scores) if polarity_scores else 0
    
    return avg_polarity, detailed_analysis

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the URL from the form submission
    url = request.form['url']
    try:
        # Fetch RSS headlines and web headlines from the provided URL
        rss_headlines = fetch_news_rss()
        web_headlines = fetch_news_web(url)  # Use the user-provided URL
        all_headlines = rss_headlines + web_headlines
        avg_sentiment, detailed_analysis = analyze_sentiment(all_headlines)

        # Prepare market opinion
        if avg_sentiment > 0.1:
            market_opinion = "Today's market sentiment is likely optimistic."
        elif avg_sentiment < -0.1:
            market_opinion = "Today's market sentiment seems bearish."
        else:
            market_opinion = "Today's market sentiment appears neutral."

        return render_template('index.html', headlines=all_headlines, analysis=detailed_analysis, opinion=market_opinion)

    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Allows access from any IP address
