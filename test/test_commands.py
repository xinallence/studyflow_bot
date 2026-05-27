"""
Unit tests for handle_command (handlers/command_handler.py)
"""
import pytest
from unittest.mock import patch, MagicMock


# ───────────────────────────────────────────────────────────────
# Хелпер: запускаємо handle_command з перехопленням stdout
# і з замоканим task_service, щоб команди не торкались диска
# ───────────────────────────────────────────────────────────────
import handlers.command_handler as ch_module


@pytest.fixture(autouse=True)
def mock_service():
    """Підмінити глобальний task_service на MagicMock для кожного тесту."""
    fake = MagicMock()
    fake.get_tasks.return_value = []
    fake.add_task.return_value = None
    fake.delete_task.return_value = True
    with patch.object(ch_module, "task_service", fake):
        yield fake


def run(cmd):
    """Запустити handle_command і повернути надрукований текст."""
    from handlers.command_handler import handle_command
    with patch("builtins.print") as mock_print:
        handle_command(cmd)
    # Збираємо всі рядки, що були надруковані
    return " ".join(str(a) for call in mock_print.call_args_list for a in call[0])


# ───────────────────────────────────────────────────────────────
# 1. start
# ───────────────────────────────────────────────────────────────
def test_start_prints_welcome():
    output = run("start")
    assert "Welcome" in output or "welcome" in output.lower()


# ───────────────────────────────────────────────────────────────
# 2. help
# ───────────────────────────────────────────────────────────────
def test_help_prints_commands():
    output = run("help")
    assert "add" in output
    assert "delete" in output


# ───────────────────────────────────────────────────────────────
# 3. add — нормальний сценарій
# ───────────────────────────────────────────────────────────────
def test_add_command_calls_service(mock_service):
    run("add Вивчити тести")
    mock_service.add_task.assert_called_once_with("Вивчити тести")


# ───────────────────────────────────────────────────────────────
# 4. add — порожній заголовок (граничний сценарій)
# ───────────────────────────────────────────────────────────────
def test_add_empty_task_shows_error(mock_service):
    output = run("add ")
    mock_service.add_task.assert_not_called()
    assert "empty" in output.lower() or "cannot" in output.lower()


# ───────────────────────────────────────────────────────────────
# 5. tasks — порожній список
# ───────────────────────────────────────────────────────────────
def test_tasks_command_empty_list(mock_service):
    mock_service.get_tasks.return_value = []
    output = run("tasks")
    assert "no tasks" in output.lower() or "not found" in output.lower() or output.strip() != ""


# ───────────────────────────────────────────────────────────────
# 6. tasks — є задачі → виводяться
# ───────────────────────────────────────────────────────────────
def test_tasks_command_shows_tasks(mock_service):
    mock_service.get_tasks.return_value = [
        {"id": 1, "title": "Задача один"},
        {"id": 2, "title": "Задача два"},
    ]
    output = run("tasks")
    assert "Задача один" in output
    assert "Задача два" in output


# ───────────────────────────────────────────────────────────────
# 7. delete — успішне видалення
# ───────────────────────────────────────────────────────────────
def test_delete_existing_task(mock_service):
    mock_service.delete_task.return_value = True
    output = run("delete 1")
    mock_service.delete_task.assert_called_once_with(1)
    assert "deleted" in output.lower()


# ───────────────────────────────────────────────────────────────
# 8. delete — неіснуюча задача
# ───────────────────────────────────────────────────────────────
def test_delete_nonexistent_task(mock_service):
    mock_service.delete_task.return_value = False
    output = run("delete 999")
    assert "not found" in output.lower()


# ───────────────────────────────────────────────────────────────
# 9. delete — некоректний id (рядок замість числа)
# ───────────────────────────────────────────────────────────────
def test_delete_invalid_id(mock_service):
    output = run("delete abc")
    mock_service.delete_task.assert_not_called()
    assert "invalid" in output.lower()


# ───────────────────────────────────────────────────────────────
# 10. невідома команда
# ───────────────────────────────────────────────────────────────
def test_unknown_command_shows_hint():
    output = run("fly_to_mars")
    assert "unknown" in output.lower() or "help" in output.lower()
