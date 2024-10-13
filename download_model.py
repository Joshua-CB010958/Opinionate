import spacy
from spacy.cli import download
from pydantic import BaseModel
from typing import List, Optional

class ModelData(BaseModel):
    name: str
    value: Optional[int] = None

def main():
    data = ModelData(name="Example", value=10)
    print(data)


def download_model():
    try:
        spacy.cli.download("en_core_web_sm")
    except Exception as e:
        print(f"Error downloading model: {e}")

def load_model():
    try:
        nlp = spacy.load("en_core_web_sm")
        print("spaCy model loaded successfully.")
    except OSError:
        print("Model not found, downloading...")
        download_model()
        nlp = spacy.load("en_core_web_sm")
        print("spaCy model downloaded and loaded successfully.")
    return nlp

if __name__ == "__main__":
    load_model()
    main()
