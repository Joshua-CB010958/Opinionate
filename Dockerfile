# Start with a lightweight Python image that includes necessary libraries
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache and install dependencies
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the SpaCy model for faster builds
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the Flask app will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
