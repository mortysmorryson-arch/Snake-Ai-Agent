import subprocess
import requests
import chromadb
from flask import Flask, request, jsonify

app = Flask(__name__)
CHROMA_PATH = "./chroma_db"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"

def get_embedding(text):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": "nomic-embed-text", "input": text}, timeout=5)
        res.raise_for_status()
        return res.json()["embeddings"][0]
    except: return []

def search_docs(query):
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_collection("snake_docs")
        vec = get_embedding(query)
        if not vec: return "Ошибка векторизации"
        results = collection.query(query_embeddings=[vec], n_results=2)
        chunks = results["documents"][0]
        return "\n---\n".join(chunks) if chunks else "Ничего не найдено"
    except Exception as e: return f"Ошибка RAG: {e}"

def git_commit(message):
    try:
        status = subprocess.run(["git", "status", "--porcelain", "index_agent.html"], capture_output=True, text=True, check=True)
        if not status.stdout.strip(): return "⚠️ Нет изменений"
        subprocess.run(["git", "add", "index_agent.html"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"feat(snake): {message}"], check=True, capture_output=True)
        return "✅ Коммит создан"
    except Exception as e: return f"❌ Git: {e}"

@app.route("/call_tool", methods=["POST"])
def call_tool():
    data = request.json
    if not data or "tool" not in data:
        return jsonify({"error": "Нужен JSON: {\"tool\": \"имя\", \"args\": {}}"}), 400
    tool = data["tool"]
    args = data.get("args", {})
    if tool == "search_docs": return jsonify({"result": search_docs(args.get("query", ""))})
    if tool == "git_commit": return jsonify({"result": git_commit(args.get("message", ""))})
    return jsonify({"error": f"Инструмент '{tool}' не найден"}), 404

if __name__ == "__main__":
    print("🚀 Сервер запущен на http://localhost:5001")
    app.run(port=5001, debug=False)
