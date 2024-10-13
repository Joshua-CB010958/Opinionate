# Use the official Python 3.8 image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download the spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application files
COPY . .

# Set the command to run your Flask application
CMD ["python", "app.py"]
