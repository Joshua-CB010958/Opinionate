# Use the official Python image from the Docker Hub with Python 3.8
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create and activate virtual environment
RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies in the virtual environment
RUN pip install --upgrade pip && pip install--no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port Flask runs on
EXPOSE 5000

# Set the command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
