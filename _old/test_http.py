# test_http.py — простой тестер для MCP-сервера
import requests
import json

BASE_URL = "http://localhost:5001"

def test_search(query: str):
    """Тестирует инструмент search_docs"""
    try:
        res = requests.post(
            f"{BASE_URL}/test/search",
            json={"query": query},
            timeout=10
        )
        if res.status_code == 200:
            return res.json()["result"]
        else:
            return f"❌ HTTP {res.status_code}: {res.text}"
    except requests.exceptions.ConnectionError:
        return "❌ Не удалось подключиться к серверу. Запущен ли mcp_server.py?"
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

def test_git(message: str):
    """Тестирует инструмент git_commit"""
    try:
        res = requests.post(
            f"{BASE_URL}/test/git",
            json={"message": message},
            timeout=10
        )
        if res.status_code == 200:
            return res.json()["result"]
        else:
            return f"❌ HTTP {res.status_code}: {res.text}"
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

if __name__ == "__main__":
    print("🔍 Тест search_docs:")
    print(test_search("как очистить canvas"))
    
    print("\n📝 Тест git_commit:")
    print(test_git("тест через python-клиент"))