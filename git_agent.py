# git_agent.py
import subprocess
import sys
from pathlib import Path

GAME_FILE = "index_agent.html"

def validate_file(path: str) -> bool:
    """Базовая проверка: файл существует и содержит основные теги"""
    p = Path(path)
    if not p.exists():
        return False
    content = p.read_text(encoding="utf-8").lower()
    return "<!doctype" in content and "</html>" in content

def git_commit(task: str) -> str:
    """Делает git add + commit с описанием задачи"""
    try:
        subprocess.run(["git", "add", GAME_FILE], check=True, capture_output=True)
        msg = f"feat(snake-agent): {task}"
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        return "✅ Коммит создан"
    except subprocess.CalledProcessError as e:
        return f"❌ Ошибка Git: {e.stderr.decode('utf-8').strip()}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python git_agent.py 'Описание задачи'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    
    if not validate_file(GAME_FILE):
        print(f"❌ Файл {GAME_FILE} не прошёл валидацию. Коммит отменён.")
        sys.exit(1)
        
    print(f"📝 Валидация пройдена. Коммичу: '{task}'...")
    print(git_commit(task))