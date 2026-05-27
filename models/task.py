class Task:
    def __init__(self, task_id, title):
        self.id = task_id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }
