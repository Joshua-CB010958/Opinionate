# Example Dockerfile setup
FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Download spaCy model
COPY download_model.py .
RUN python download_model.py

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

