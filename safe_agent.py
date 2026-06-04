# safe_agent.py — безопасная генерация патчей (не ломает базу)
import requests, sys, re
from pathlib import Path

RAG_URL = "http://localhost:5001/call_tool"
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"
BASE = "index.html"
OUT = "index_agent.html"

def rag(q):
    try:
        r = requests.post(RAG_URL, json={"tool":"search_docs","args":{"query":q}}, timeout=5)
        return r.json().get("result","")
    except: return ""

def gen(task, ctx):
    prompt = f"""Ты JS-разработчик. Задача: {task}
Контекст из доков: {ctx}
ВЕРНИ ТОЛЬКО <script>...</script> с решением. Не пиши HTML, CSS, не меняй игру.
Используй точные API из контекста. Вывод:"""
    r = requests.post(OLLAMA, json={"model":MODEL,"prompt":prompt,"stream":False,"options":{"temperature":0.05,"num_ctx":4096}})
    code = r.json().get("response","").strip()
    if "```" in code: code = code.split("```")[1].strip()
    return code

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Использование: python safe_agent.py 'задача'"); sys.exit(1)
    task = " ".join(sys.argv[1:])
    ctx = rag(task)
    patch = gen(task, ctx)
    if "<script>" not in patch: patch = f"<script>\n{patch}\n</script>"
    html = Path(BASE).read_text(encoding="utf-8")
    html = html.replace("</body>", f"\n{patch}\n</body>")
    Path(OUT).write_text(html, encoding="utf-8")
    print("✅ Патч вставлен в", OUT)