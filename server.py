import subprocess
import requests
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn

app = FastAPI(
    title="Snake AI Agent - MCP Server",
    description="HTTP-сервер инструментов для ИИ-агента: семантический поиск по документации и Git-автоматизация.",
    version="1.0.0"
)

CHROMA_PATH = "./chroma_db"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"


# --- Pydantic-модели (валидация + автоматическая документация) ---

class ToolRequest(BaseModel):
    tool: str = Field(..., description="Имя инструмента: 'search_docs' или 'git_commit'")
    args: Optional[Dict[str, Any]] = Field(default={}, description="Аргументы для инструмента")

class ToolResponse(BaseModel):
    result: str

class ErrorResponse(BaseModel):
    error: str


# --- Вспомогательные функции (без изменений) ---

def get_embedding(text):
    try:
        res = requests.post(
            OLLAMA_EMBED_URL,
            json={"model": "nomic-embed-text", "input": text},
            timeout=5
        )
        res.raise_for_status()
        return res.json()["embeddings"][0]
    except:
        return []

def search_docs(query):
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_collection("snake_docs")
        vec = get_embedding(query)
        if not vec:
            return "Ошибка векторизации"
        results = collection.query(query_embeddings=[vec], n_results=2)
        chunks = results["documents"][0]
        return "\n---\n".join(chunks) if chunks else "Ничего не найдено"
    except Exception as e:
        return f"Ошибка RAG: {e}"

def git_commit(message):
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain", "index_agent.html"],
            capture_output=True, text=True, check=True
        )
        if not status.stdout.strip():
            return "⚠️ Нет изменений"
        subprocess.run(["git", "add", "index_agent.html"], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"feat(snake): {message}"],
            check=True, capture_output=True
        )
        return "✅ Коммит создан"
    except Exception as e:
        return f"❌ Git: {e}"


# --- Эндпоинты ---

@app.post(
    "/call_tool",
    response_model=ToolResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        404: {"model": ErrorResponse, "description": "Инструмент не найден"}
    },
    summary="Вызов инструмента агента",
    description="Основной эндпоинт для взаимодействия ИИ-агента с внешними инструментами (MCP-концепция)."
)
def call_tool(data: ToolRequest):
    tool = data.tool
    args = data.args or {}

    if tool == "search_docs":
        return ToolResponse(result=search_docs(args.get("query", "")))
    if tool == "git_commit":
        return ToolResponse(result=git_commit(args.get("message", "")))
    
    raise HTTPException(status_code=404, detail=f"Инструмент '{tool}' не найден")


@app.get("/health", summary="Проверка работоспособности")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    print("🚀 Сервер запущен на http://localhost:5001")
    print("📖 Swagger-документация: http://localhost:5001/docs")
    uvicorn.run(app, host="127.0.0.1", port=5001, log_level="info")