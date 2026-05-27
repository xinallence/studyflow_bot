from services.task_service import TaskService

task_service = TaskService()


def show_help():
    print("""
Available commands:
start                - start bot
help                 - show commands
add <task>           - add new task
tasks                - show all tasks
delete <id>          - delete task
exit                 - stop bot
""")


def handle_command(command):
    if command == "start":
        print("Welcome to StudyFlow Bot!")

    elif command == "help":
        show_help()

    elif command.startswith("add "):
        task_text = command[4:].strip()

        if not task_text:
            print("Task cannot be empty.")
            return

        task_service.add_task(task_text)
        print("Task added successfully.")

    elif command == "tasks":
        tasks = task_service.get_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            print(f"{task['id']}. {task['title']}")

    elif command.startswith("delete "):
        try:
            task_id = int(command.split()[1])
            result = task_service.delete_task(task_id)

            if result:
                print("Task deleted.")
            else:
                print("Task not found.")

        except (IndexError, ValueError):
            print("Invalid task ID.")

    else:
        print("Unknown command. Type 'help'.")
