import json
from pathlib import Path


class TaskService:
    def __init__(self, data_file="data/tasks.json"):
        self.data_file = Path(data_file)
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not self.data_file.exists():
            return []

        with open(self.data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_tasks(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
        }

        self.tasks.append(task)
        self.save_tasks()

        return task

    def get_tasks(self):
        return self.tasks

    def delete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True

        return False