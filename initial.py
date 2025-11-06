from typing import Callable, Any, Dict, Tuple, List, Optional


def input_error(func: Callable) -> Callable:
    def inner(cmd: str, *args: Any, **kwargs: Any) -> Optional[str]:
        invalid_arguments_messages = {
            "add": "Invalid arguments. Usage: add <name> <phone>",
            "change": "Invalid arguments. Usage: change <name> <phone>",
            "phone": "Invalid arguments. Usage: phone <name>",
            "all": "Invalid arguments. Usage: all"
        }

        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError, TypeError):
            return invalid_arguments_messages.get(cmd)
        except Exception as e:
            return f"Error occurred: {e}"

    return inner


def parse_input(user_input: str) -> Tuple[str, ...] | None:
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args
    except ValueError:
        return None


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    name, phone = args

    if name in contacts:
        return f"The name {name} is already exists on your contacts list."
    else:
        contacts[name] = phone
        return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    name, phone = args

    if name in contacts:
        contacts[name] = phone
        return "Contact changed."
    else:
        return "Contact not found"


@input_error
def display_phone(args: List[str], contacts: Dict[str, str]) -> str:
    name = args[0]
    current_contact = contacts.get(name)
    return current_contact or "Contact not found"


@input_error
def display_all_contacts(contacts: Dict[str, str]) -> str:
    result = ""

    if len(contacts) == 0:
        return "Your contact list is empty."
    else:
        for name, phone in contacts.items():
            result += f"{name}: {phone} \n"
        return result.rstrip("\n")


def main() -> None:
    """
    Assistant Bot

    This bot helps manage a simple contact list via command-line interaction.
    Users can add, change, view, and list contacts using text commands.

    Available commands and their functions:
    - hello: Greets the user.
    - add <name> <phone>: Adds a new contact with the specified name and
        phone number.
    - change <name> <phone>: Changes the phone number for an existing contact.
    - phone <name>: Displays the phone number for the specified contact.
    - all: Shows all contacts in the list.
    - exit / close: Exits the bot.
    """

    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        parsed = parse_input(user_input)
        if not parsed:
            print("Invalid command.")
            continue

        command, *args = parsed

        match command:
            case "exit" | "close":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(command, args, contacts))
            case "change":
                print(change_contact(command, args, contacts))
            case "phone":
                print(display_phone(command, args, contacts))
            case "all":
                print(display_all_contacts(command, contacts))
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
