import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))


# Тест 1: RAG возвращает строку при успешном ответе
@patch('safe_agent.requests.post')
def test_rag_returns_string(mock_post):
    """Функция rag() должна возвращать строку при успехе"""
    from safe_agent import rag
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "какой-то контекст из доков"}
    mock_post.return_value = mock_response
    
    result = rag("тестовый запрос")
    assert isinstance(result, str), "RAG должен возвращать строку"
    assert result == "какой-то контекст из доков", "Должен вернуть то, что прислал сервер"


# Тест 2: RAG не падает при недоступном сервере
@patch('safe_agent.requests.post')
def test_rag_handles_server_error(mock_post):
    """Функция rag() не должна падать, если сервер недоступен"""
    from safe_agent import rag
    
    mock_post.side_effect = Exception("Connection refused")
    
    result = rag("тестовый запрос")
    assert result == "", "При ошибке RAG должен возвращать пустую строку"


# Тест 3: gen() возвращает строку с кодом
@patch('safe_agent.requests.post')
def test_gen_returns_code(mock_post):
    """Функция gen() должна возвращать сгенерированный код"""
    from safe_agent import gen
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "<script>alert('test');</script>"}
    mock_post.return_value = mock_response
    
    result = gen("добавь кнопку", "контекст из доков")
    assert isinstance(result, str), "gen() должен возвращать строку"
    assert "<script>" in result, "Должен содержать сгенерированный код"


# Тест 4: gen() очищает markdown-обёртки от ответа модели
@patch('safe_agent.requests.post')
def test_gen_cleans_markdown(mock_post):
    """Функция gen() должна убирать ``` из ответа модели"""
    from safe_agent import gen
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "```html\n<script>test</script>\n```"}
    mock_post.return_value = mock_response
    
    result = gen("задача", "контекст")
    assert "```" not in result, "Markdown-обёртки должны быть удалены"
    assert "<script>" in result, "Сам код должен остаться"