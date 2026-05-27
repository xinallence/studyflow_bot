from handlers.command_handler import handle_command


def main():
    print("StudyFlow Bot started!")
    print("Type 'help' to see available commands.")

    while True:
        command = input(">> ").strip()

        if command.lower() == "exit":
            print("Bot stopped.")
            break

        handle_command(command)


if __name__ == "__main__":
    main()
