# test_client.py — простой клиент для проверки MCP-сервера
import subprocess
import json
import sys

def call_tool(tool_name: str, args: dict):
    """Отправляет запрос к MCP-серверу через stdio"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    }
    
    proc = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, cwd="."
    )
    
    # Отправляем запрос
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.close()
    
    # Читаем ответ (пропускаем служебные сообщения)
    for line in proc.stdout:
        line = line.strip()
        if line.startswith("{") and '"result"' in line:
            try:
                res = json.loads(line)
                return res["result"]["content"][0]["text"]
            except:
                pass
    return "Не удалось получить ответ"

if __name__ == "__main__":
    print("🔍 Тест search_docs:")
    print(call_tool("search_docs", {"query": "как очистить canvas"}))
    
    print("\n📝 Тест git_commit:")
    print(call_tool("git_commit", {"message": "тест mcp через клиент"}))