import os
import requests
import chromadb
from pathlib import Path

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "snake_docs"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
CHUNK_SIZE = 300

def get_embedding(text):
    """Запрашивает вектор у локальной Ollama"""
    res = requests.post(OLLAMA_EMBED_URL, json={"model": "nomic-embed-text", "input": text})
    res.raise_for_status()
    return res.json()["embeddings"][0]

def chunk_text(text):
    """Разбивает текст на фрагменты по ~300 символов"""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for p in paragraphs:
        if len(p) <= CHUNK_SIZE:
            chunks.append(p)
        else:
            for i in range(0, len(p), CHUNK_SIZE):
                chunks.append(p[i:i+CHUNK_SIZE])
    return chunks

def main():
    print("🚀 Инициализация базы данных...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)
    
    docs_dir = Path("./docs")
    if not docs_dir.exists():
        print("❌ Папка docs/ не найдена. Убедись, что скрипт лежит в корневой папке snake-rag/")
        return

    print("📖 Индексация документов...")
    total = 0
    
    for file_path in docs_dir.glob("*.md"):
        print(f"  → Обработка {file_path.name}...")
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        
        if not chunks: continue
            
        ids = [f"{file_path.stem}_{i}" for i in range(len(chunks))]
        embeddings = [get_embedding(c) for c in chunks]
        
        collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"source": file_path.name} for _ in chunks]
        )
        total += len(chunks)

    print(f"✅ Готово. Загружено {total} фрагментов в коллекцию '{COLLECTION_NAME}'.")
    print(f"💾 База сохранена: {os.path.abspath(CHROMA_PATH)}")

if __name__ == "__main__":
    main()