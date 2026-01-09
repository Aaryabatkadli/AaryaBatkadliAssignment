import os
import json

# Build the correct file path regardless of OS
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "data", "product_description.json")

def load_products():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)
