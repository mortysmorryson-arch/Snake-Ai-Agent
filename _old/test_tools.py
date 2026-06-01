import requests

def call_tool(tool: str, args: dict):
    res = requests.post("http://localhost:5001/call_tool", json={"tool": tool, "args": args}, timeout=10)
    return res.json()

if __name__ == "__main__":
    print("🔍 Тест RAG:")
    print(call_tool("search_docs", {"query": "как очистить canvas"})["result"])
    
    print("\n📝 Тест Git:")
    print(call_tool("git_commit", {"message": "тест через новый сервер"})["result"])