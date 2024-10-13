from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


app = Flask(__name__)

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

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
    return polarity

def get_summary(text):
    # Generate a summary of the content using spaCy
    doc = nlp(text)
    sentences = list(doc.sents)

    # Get the top sentences based on their importance
    if len(sentences) <= 2:
        return text  # Return full text if too short

    # Select the most important sentences (e.g., first 2 sentences for brevity)
    summary_sentences = sentences[:2]
    summary = ' '.join([sent.text for sent in summary_sentences])
    
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

if __name__ == '__main__':
    app.run(debug=True)
    load_model()
