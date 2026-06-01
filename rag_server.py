# rag_server.py — простой HTTP-сервер для поиска по базе знаний
from flask import Flask, request, jsonify
import chromadb
import requests

app = Flask(__name__)
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "snake_docs"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"

def get_embedding(text):
    res = requests.post(OLLAMA_EMBED_URL, json={"model": "nomic-embed-text", "input": text})
    return res.json()["embeddings"][0]

@app.route("/search", methods=["POST"])
def search():
    """Поиск релевантных фрагментов по запросу"""
    query = request.json.get("query", "")
    top_k = request.json.get("top_k", 2)
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    
    query_vec = get_embedding(query)
    results = collection.query(query_embeddings=[query_vec], n_results=top_k)
    
    return jsonify({
        "chunks": results["documents"][0],
        "sources": [m["source"] for m in results["metadatas"][0]]
    })

if __name__ == "__main__":
    print("🚀 RAG-сервер запущен на http://localhost:5000")
    app.run(port=5000, debug=False)