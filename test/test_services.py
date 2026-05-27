import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import tempfile
import os


@pytest.fixture
def tmp_task_dir(tmp_path):
    return tmp_path


@pytest.fixture
def service(tmp_task_dir):
    from services.task_service import TaskService
    svc = TaskService(data_file=str(tmp_task_dir / "tasks.json"))
    return svc


def test_add_task_increases_count(service):
    service.add_task("Вивчити Python")
    assert len(service.tasks) == 1


def test_add_task_stores_correct_title(service):
    service.add_task("Прочитати лекцію")
    assert service.tasks[0]["title"] == "Прочитати лекцію"


def test_add_multiple_tasks_unique_ids(service):
    service.add_task("Задача A")
    service.add_task("Задача B")
    service.add_task("Задача C")
    ids = [t["id"] for t in service.tasks]
    assert len(ids) == len(set(ids)), "id-и задач мають бути унікальними"


def test_get_tasks_empty_initially(service):
    assert service.get_tasks() == []


def test_get_tasks_returns_all(service):
    service.add_task("Перша")
    service.add_task("Друга")
    assert len(service.get_tasks()) == 2


def test_delete_task_success(service):
    service.add_task("Видалити мене")
    task_id = service.tasks[0]["id"]
    result = service.delete_task(task_id)
    assert result is True
    assert len(service.tasks) == 0


def test_delete_task_nonexistent_returns_false(service):
    service.add_task("Залишитись")
    result = service.delete_task(9999)
    assert result is False
    assert len(service.tasks) == 1


def test_tasks_persisted_to_file(tmp_task_dir):
    from services.task_service import TaskService
    svc = TaskService(data_file=str(tmp_task_dir / "tasks.json"))
    svc.add_task("Збережена задача")
    file_path = tmp_task_dir / "tasks.json"
    raw = json.loads(file_path.read_text(encoding="utf-8"))
    assert len(raw) == 1
    assert raw[0]["title"] == "Збережена задача"


def test_load_tasks_missing_file(tmp_path):
    from services.task_service import TaskService
    missing_file = tmp_path / "nonexistent.json"
    svc = TaskService(data_file=str(missing_file))
    assert svc.tasks == []


def test_delete_one_of_many_tasks(service):
    service.add_task("Задача 1")
    service.add_task("Задача 2")
    service.add_task("Задача 3")
    id_to_delete = service.tasks[1]["id"]
    service.delete_task(id_to_delete)
    remaining_titles = [t["title"] for t in service.tasks]
    assert "Задача 2" not in remaining_titles
    assert "Задача 1" in remaining_titles
    assert "Задача 3" in remaining_titles
