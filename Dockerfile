# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download TextBlob corpora and NLTK data
RUN python -m textblob.download_corpora
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
