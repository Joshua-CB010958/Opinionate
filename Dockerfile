# Use the official Python image from Docker Hub with Python 3.9
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file first to cache dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the SpaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application files
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Set the command to run the application
CMD ["python", "app.py"]
