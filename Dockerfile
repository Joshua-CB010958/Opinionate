# Use the official Python image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .

# Install virtualenv
RUN pip install --upgrade pip && pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Install dependencies inside the virtual environment
RUN . venv/bin/activate && pip install -r requirements.txt

# Copy the rest of your application files
COPY . .

# Set the entry point for the container
CMD ["python", "app.py"]
