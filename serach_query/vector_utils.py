from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, products, top_k=3):
    texts = [p["text"] for p in products]

    product_embeddings = model.encode(texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, product_embeddings)[0]

    results = []
    for i, score in enumerate(scores):
        results.append({
            "id": products[i]["id"],
            "text": products[i]["text"],
            "score": float(score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
