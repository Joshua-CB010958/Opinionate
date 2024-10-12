# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port Flask runs on
EXPOSE 5000

# Set the command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
