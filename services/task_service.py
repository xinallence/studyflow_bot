import json
from pathlib import Path

DATA_FILE = Path("data/tasks.json")


class TaskService:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not DATA_FILE.exists():
            return []

        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
        }

        self.tasks.append(task)
        self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def delete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True

        return False
