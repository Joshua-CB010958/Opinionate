# Use the official Python 3.8 image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the download script to download the spaCy model
COPY download_model.py .

# Download the spaCy model
RUN python download_model.py

# Copy the rest of your application files
COPY . .

# Set the command to run your Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
