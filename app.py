from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

app = Flask(__name__)

# Define positive and negative keywords
positive_keywords = ['good', 'great', 'positive', 'improved', 'success', 'benefit', 'advantage', 'achievement', 'hope', 'rise']
negative_keywords = ['bad', 'poor', 'negative', 'declined', 'failure', 'disadvantage', 'crisis', 'struggle', 'drop', 'loss', 'below']

def fetch_article_content(url):
    try:
        # Set a user-agent header to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
        }

        # Web scrape the article from the provided URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the main content (update the selectors based on the website structure)
        title = soup.find('h1').text.strip() if soup.find('h1') else 'No Title Found'
        paragraphs = soup.find_all('p')
        content = ' '.join([para.text.strip() for para in paragraphs if para.text.strip()])

        if not content:
            return title, "No content found in the article."

        return title, content
    except Exception as e:
        return "Error", str(e)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity  # -1 to +1 (negative to positive)

    # Adjust sentiment score based on keywords
    for word in positive_keywords:
        if word in text.lower():
            polarity += 0.1  # Increase score for positive words
    for word in negative_keywords:
        if word in text.lower():
            polarity -= 0.1  # Decrease score for negative words

    # Ensure the polarity score stays within the range of -1 to +1
    polarity = max(-1, min(1, polarity))

    return polarity

def get_summary(text):
    # Use TextBlob's sentence tokenization
    blob = TextBlob(text)
    sentences = blob.sentences
    
    # If there are fewer than 5 sentences, return the original text trimmed
    if len(sentences) <= 5:
        return text[:250] + '...'  # Fallback to a trimmed version if too short

    # Create a simple ranking based on sentence polarity and length
    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = sentence.sentiment.polarity * len(sentence)

    # Sort sentences by their score
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Select top sentences for the summary
    summary_sentences = sorted_sentences[:5]  # Get top 5 sentences
    summary = ' '.join(str(sent) for sent in summary_sentences)

    return summary

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the URL from the form submission
    url = request.form['url']
    try:
        # Fetch article title and content from the provided URL
        title, content = fetch_article_content(url)

        # Check if there was an error fetching content
        if content.startswith("Error"):
            raise ValueError(content)

        if not content or 'No Title Found' in title:
            raise ValueError("No valid content found at the provided URL.")

        # Analyze sentiment of the full content
        avg_sentiment = analyze_sentiment(content)

        # Get summary of the content
        summary = get_summary(content)

        # Prepare daily summary based on sentiment
        if avg_sentiment > 0.1:
            daily_summary = "Today's summary indicates a positive sentiment in the news articles."
        elif avg_sentiment < -0.1:
            daily_summary = "Today's summary indicates a negative sentiment in the news articles."
        else:
            daily_summary = "Today's summary indicates a neutral sentiment in the news articles."

        return render_template('index.html', title=title, summary=summary, sentiment=daily_summary)

    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
