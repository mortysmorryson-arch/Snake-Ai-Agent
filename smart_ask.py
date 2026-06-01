# smart_ask.py — задаёт вопрос ИИ с подтягиванием контекста из RAG
import requests
import sys

RAG_API = "http://localhost:5000/search"
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

def get_rag_context(query, top_k=2):
    """Запрашивает контекст у нашего RAG-сервера"""
    try:
        res = requests.post(RAG_API, json={"query": query, "top_k": top_k}, timeout=5)
        if res.status_code == 200:
            chunks = res.json().get("chunks", [])
            return "\n---\n".join(chunks)
    except:
        pass
    return ""

def ask_ai(question):
    """Запрашивает ответ у локальной модели с контекстом"""
    context = get_rag_context(question)
    
    if context:
        prompt = f"""Ты помощник по разработке игр. Отвечай ТОЛЬКО на основе контекста ниже.
Если ответа нет — скажи "Нет данных в базе".
Используй точные названия методов.

Контекст:
{context}

Вопрос: {question}
Ответ:"""
    else:
        prompt = f"Вопрос: {question}\nОтвет:"

    res = requests.post(OLLAMA_API, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    })
    return res.json().get("response", "Ошибка").strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python smart_ask.py 'Ваш вопрос'")
    else:
        q = sys.argv[1]
        print(f"🤖 {ask_ai(q)}")