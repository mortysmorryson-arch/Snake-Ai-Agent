@echo off
chcp 65001 >nul
echo.
echo === Змейка + ИИ-агент (Демо) ===
echo.
cd /d "%~dp0"

echo [1] Проверка зависимостей...
python -m pip install -r requirements.txt -q 2>nul

echo [2] Проверка Ollama...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo Ollama не найдена. Скачай: https://ollama.com/download
    pause & exit /b
)

echo [3] Загрузка моделей...
ollama ls | findstr "nomic-embed-text" >nul
if %errorlevel% neq 0 ollama pull nomic-embed-text
ollama ls | findstr "qwen2.5-coder:7b" >nul
if %errorlevel% neq 0 ollama pull qwen2.5-coder:7b

echo [4] Запуск Ollama...
start /min "" ollama serve
timeout /t 3 /nobreak >nul

echo [5] Индексация документации...
if not exist "chroma_db" python ingest.py

echo [6] Запуск сервера инструментов...
start /min "" python server.py
timeout /t 3 /nobreak >nul

echo.
set /p TASK="📝 Задача (или Enter для демо): "
if "%TASK%"=="" set TASK=Добавь паузу по клавише P с текстом ПАУЗА

echo [7] Генерация...
python safe_agent.py "%TASK%"
if %errorlevel% neq 0 (
    echo ❌ Агент упал. Проверь, запущен ли server.py и ollama.
    pause & exit /b
)

if exist "index_agent.html" (
    echo ✅ Готово! Открываю...
    start index_agent.html
) else (
    echo ❌ Файл не создан.
)
echo.
pause