import requests
import chromadb
import sys

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "snake_docs"
OLLAMA_API = "http://localhost:11434/api"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen2.5-coder:7b"

def get_embedding(text):
    """Получает вектор запроса"""
    res = requests.post(f"{OLLAMA_API}/embed", json={"model": EMBED_MODEL, "input": text})
    res.raise_for_status()
    return res.json()["embeddings"][0]

def search_context(query, top_k=2):
    """Ищет релевантные фрагменты в базе"""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    
    query_vec = get_embedding(query)
    results = collection.query(query_embeddings=[query_vec], n_results=top_k)
    return "\n---\n".join(results["documents"][0])

def generate_answer(context, question):
    """Отправляет промпт с контекстом в локальную модель"""
    prompt = f"""Ты технический помощник. Отвечай ТОЛЬКО на основе предоставленного контекста.
Если ответа нет в контексте, скажи: "Нет данных в базе знаний".
Используй точные названия методов.

Контекст:
{context}

Вопрос: {question}
Ответ:"""

    res = requests.post(f"{OLLAMA_API}/generate", json={
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    })
    res.raise_for_status()
    return res.json()["response"].strip()

def main():
    if len(sys.argv) < 2:
        print("Использование: python ask_rag.py 'Ваш вопрос в кавычках'")
        return

    query = sys.argv[1]
    print(f"🔍 Поиск по базе: '{query}'...")
    
    context = search_context(query)
    if not context or context.strip() == "":
        print("❌ Ничего не найдено в базе.")
        return

    print(f"📄 Найденный контекст:\n{context[:200]}...\n")
    print("🤖 Генерация ответа (локальная модель)...")
    print("="*40)
    print(generate_answer(context, query))
    print("="*40)

if __name__ == "__main__":
    main()