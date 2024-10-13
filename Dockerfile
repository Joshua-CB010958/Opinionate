FROM python:3.8-slim

WORKDIR /app

# Copy only requirements file first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the spaCy model (assumed to be in the same directory)
COPY en_core_web_sm-3.1.0 /usr/local/lib/python3.8/site-packages/en_core_web_sm

# Now copy the rest of the application
COPY . .

ENV FLASK_APP=app.py
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
