# Use the official Python image from the Docker Hub with Python 3.8
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .

# Install virtualenv
RUN pip install --upgrade pip && \
    pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install the dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port Flask runs on
EXPOSE 5000

# Set the command to run the application
CMD ["venv/bin/python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
