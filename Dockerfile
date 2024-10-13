# Use the official Python 3.8 image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first
COPY requirements.txt ./

# Install virtualenv
RUN pip install --upgrade pip && pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies, suppressing warnings
RUN . venv/bin/activate && pip install --root-user-action=ignore -r requirements.txt

# Download the spaCy model
RUN . venv/bin/activate && python -m spacy download en_core_web_sm

# Copy the download script to download the spaCy model
COPY download_model.py .

# Uncomment to run the download script if needed
# RUN . venv/bin/activate && python download_model.py

# Copy the rest of your application files
COPY . .

# Set the command to run your Flask application, ensuring the venv is activated
CMD ["venv/bin/python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
