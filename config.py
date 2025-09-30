import os
DATA_ = "./data"
RAW_CSV = os.path.join(DATA_, "books_data.csv")
CLEAN_CSV = os.path.join(DATA_, "clean_books.csv")
MODEL_PATH = os.path.join(DATA_, "price_model.pt")
META_PATH = os.path.join(DATA_, "model_meta.json")
BASE_URL = "https://books.toscrape.com" 
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
os.makedirs(DATA_, exist_ok=True)