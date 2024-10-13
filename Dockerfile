# Use the official Python 3.8 image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt .

# Upgrade pip and install the requirements globally (no virtualenv needed)
RUN pip install --upgrade pip --no-warn-script-location && \
    pip install --root-user-action=ignore -r requirements.txt --no-warn-script-location

# Download the spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application files
COPY . .

# Set the command to run your Flask application
CMD ["python", "your_flask_app.py"]
