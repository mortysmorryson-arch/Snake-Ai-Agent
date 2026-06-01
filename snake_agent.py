# snake_agent.py v2
import requests
import sys
import os
from pathlib import Path

RAG_API = "http://localhost:5000/search"
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"
GAME_FILE = "index.html"
OUTPUT_FILE = "index_agent.html"

def get_rag_context(query):
    try:
        res = requests.post(RAG_API, json={"query": query, "top_k": 2}, timeout=5)
        if res.status_code == 200:
            return "\n---\n".join(res.json().get("chunks", []))
    except:
        pass
    return ""

def get_current_code():
    if os.path.exists(GAME_FILE):
        return Path(GAME_FILE).read_text(encoding="utf-8")
    return "<!-- Файл не найден -->"

def agent_generate(task):
    print(f"🔍 1. Ищу технический контекст...")
    context = get_rag_context(task)
    
    current_code = get_current_code()
    print(f"📄 Загружен текущий код ({len(current_code)} символов)")
    print(f"🤖 2. Генерирую код (модель {MODEL})...")

    system_prompt = """Ты Senior Frontend Engineer. Твоя задача — ИНТЕГРИРОВАТЬ новую фичу в существующий файл.
ЗАПРЕЩЕНО: удалять текущую логику, использовать заглушки "// ...остальной код", сокращать стили или HTML.
ОБЯЗАНО: вернуть ПОЛНЫЙ валидный файл от <!DOCTYPE html> до </html>."""

    prompt = f"""<TASK>
{task}
</TASK>

<DOCUMENTATION_CONTEXT>
{context}
</DOCUMENTATION_CONTEXT>

<EXISTING_CODE>
{current_code}
</EXISTING_CODE>

<RULES>
1. Внимательно прочитай <EXISTING_CODE>.
2. Добавь функционал из <TASK>, используя <DOCUMENTATION_CONTEXT>.
3. СОХРАНИ ВСЁ: змейку, управление, паузу, рекорды, звуки, ускорение, CSS, canvas.
4. Верни ТОЛЬКО готовый код. Начинай строго с <!DOCTYPE html>.
5. Никаких markdown, пояснений или текста вне кода.
</RULES>"""

    res = requests.post(OLLAMA_API, json={
        "model": MODEL,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 16384}
    })
    res.raise_for_status()
    return res.json().get("response", "").strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python snake_agent.py 'Опиши новую фичу'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    code = agent_generate(task)

    if code and "<!DOCTYPE" in code.upper():
        # Чистка от markdown, если модель всё же добавила обёртку
        if "```html" in code.lower():
            code = code.split("```html")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].strip()
            
        Path(OUTPUT_FILE).write_text(code, encoding="utf-8")
        print(f"✅ 3. Готово! Файл сохранён: {OUTPUT_FILE}")
        print("📝 Замени index.html на index_agent.html и открой в браузере.")
    else:
        print("❌ Ошибка: модель не вернула валидный HTML.")
        print("💡 Проверь, запущены ли rag_server.py и ollama. Попробуй упростить задачу.")# snake_agent.py v2
import requests
import sys
import os
from pathlib import Path

RAG_API = "http://localhost:5000/search"
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"
GAME_FILE = "index.html"
OUTPUT_FILE = "index_agent.html"

def get_rag_context(query):
    try:
        res = requests.post(RAG_API, json={"query": query, "top_k": 2}, timeout=5)
        if res.status_code == 200:
            return "\n---\n".join(res.json().get("chunks", []))
    except:
        pass
    return ""

def get_current_code():
    if os.path.exists(GAME_FILE):
        return Path(GAME_FILE).read_text(encoding="utf-8")
    return "<!-- Файл не найден -->"

def agent_generate(task):
    print(f"🔍 1. Ищу технический контекст...")
    context = get_rag_context(task)
    
    current_code = get_current_code()
    print(f"📄 Загружен текущий код ({len(current_code)} символов)")
    print(f"🤖 2. Генерирую код (модель {MODEL})...")

    system_prompt = """Ты Senior Frontend Engineer. Твоя задача — ИНТЕГРИРОВАТЬ новую фичу в существующий файл.
ЗАПРЕЩЕНО: удалять текущую логику, использовать заглушки "// ...остальной код", сокращать стили или HTML.
ОБЯЗАНО: вернуть ПОЛНЫЙ валидный файл от <!DOCTYPE html> до </html>."""

    prompt = f"""<TASK>
{task}
</TASK>

<DOCUMENTATION_CONTEXT>
{context}
</DOCUMENTATION_CONTEXT>

<EXISTING_CODE>
{current_code}
</EXISTING_CODE>

<RULES>
1. Внимательно прочитай <EXISTING_CODE>.
2. Добавь функционал из <TASK>, используя <DOCUMENTATION_CONTEXT>.
3. СОХРАНИ ВСЁ: змейку, управление, паузу, рекорды, звуки, ускорение, CSS, canvas.
4. Верни ТОЛЬКО готовый код. Начинай строго с <!DOCTYPE html>.
5. Никаких markdown, пояснений или текста вне кода.
</RULES>"""

    res = requests.post(OLLAMA_API, json={
        "model": MODEL,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 16384}
    })
    res.raise_for_status()
    return res.json().get("response", "").strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python snake_agent.py 'Опиши новую фичу'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    code = agent_generate(task)

    if code and "<!DOCTYPE" in code.upper():
        # Чистка от markdown, если модель всё же добавила обёртку
        if "```html" in code.lower():
            code = code.split("```html")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].strip()
            
        Path(OUTPUT_FILE).write_text(code, encoding="utf-8")
        print(f"✅ 3. Готово! Файл сохранён: {OUTPUT_FILE}")
        print("📝 Замени index.html на index_agent.html и открой в браузере.")
    else:
        print("❌ Ошибка: модель не вернула валидный HTML.")
        print("💡 Проверь, запущены ли rag_server.py и ollama. Попробуй упростить задачу.")