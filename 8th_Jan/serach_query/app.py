from fastapi import FastAPI
from routes.products import router as product_router

app = FastAPI(title="Product Semantic Search API")

app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "API running"}
