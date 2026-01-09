from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data_loader import load_products, save_products

router = APIRouter(prefix="/products", tags=["Products"])

# -------------------- SCHEMAS --------------------

class Product(BaseModel):
    id: int
    text: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

# -------------------- DATA --------------------

products = load_products()

# -------------------- CRUD OPERATIONS --------------------

@router.get("/", response_model=List[Product])
def get_products():
    return products

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/", response_model=Product)
def create_product(product: Product):
    for p in products:
        if p["id"] == product.id:
            raise HTTPException(status_code=400, detail="Product ID already exists")

    products.append(product.dict())
    save_products(products)
    return product

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products[i] = product.dict()
            save_products(products)
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{product_id}")
def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            deleted = products.pop(i)
            save_products(products)
            return deleted
    raise HTTPException(status_code=404, detail="Product not found")

# -------------------- SEMANTIC SEARCH --------------------

@router.post("/search")
def semantic_search(req: SearchRequest):
    if not products:
        return {"query": req.query, "results": []}

    texts = [p["text"] for p in products]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(texts + [req.query])

    product_vectors = vectors[:-1]
    query_vector = vectors[-1]

    scores = cosine_similarity(query_vector, product_vectors)[0]
    top_indices = scores.argsort()[-req.top_k:][::-1]

    results = [
        {
            "id": products[i]["id"],
            "text": products[i]["text"],
            "score": float(scores[i])
        }
        for i in top_indices
        if scores[i] > 0
    ]

    return {
        "query": req.query,
        "results": results
    }
