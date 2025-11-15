import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from difflib import get_close_matches
import os

"File for storing data"
DATA_FILE = "data.json"

"Data initialization"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"contacts": [], "notes": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


data = load_data()

"Dictionary of commands"
COMMANDS = {
    'add contact': 'Add a contact',
    'list contacts': 'List all contacts',
    'search contacts': 'Search contacts',
    'edit contact': 'Edit a contact',
    'delete contact': 'Delete a contact',
    'birthdays': 'Birthdays in X days',
    'add note': 'Add a note',
    'list notes': 'List notes',
    'search notes': 'Search notes',
    'edit note': 'Edit a note',
    'delete note': 'Delete a note',
    'exit': 'Exit'
}

command_completer = WordCompleter(list(COMMANDS.keys()), ignore_case=True)

"Functions for working with contacts"


def add_contact():
    name = prompt("Name: ")
    phone = prompt("Phone: ")
    data["contacts"].append({"name": name, "phone": phone})
    save_data(data)
    print(f"✅ Contact {name} added.")


def list_contacts():
    if not data["contacts"]:
        print("No contacts yet.")
    for c in data["contacts"]:
        print(f"{c['name']} - {c['phone']}")


def search_contacts():
    query = prompt("Search name: ")
    results = [c for c in data["contacts"]
               if query.lower() in c["name"].lower()]
    if results:
        for c in results:
            print(f"{c['name']} - {c['phone']}")
    else:
        print("No matches found.")


def edit_contact():
    name = prompt("Enter name to edit: ")
    for c in data["contacts"]:
        if c["name"].lower() == name.lower():
            new_phone = prompt("New phone: ")
            c["phone"] = new_phone
            save_data(data)
            print(f"✏️ Contact {name} updated.")
            return
    print("Contact not found.")


def delete_contact():
    name = prompt("Enter name to delete: ")
    data["contacts"] = [c for c in data["contacts"]
                        if c["name"].lower() != name.lower()]
    save_data(data)
    print(f"🗑️ Contact {name} deleted.")


def birthdays():
    print("🎂 (Demo) Birthday reminders not implemented yet.")


"Functions for working with notes"


def add_note():
    title = prompt("Note title: ")
    content = prompt("Note content: ")
    data["notes"].append({"title": title, "content": content})
    save_data(data)
    print(f"✅ Note '{title}' added.")


def list_notes():
    if not data["notes"]:
        print("No notes yet.")
    for n in data["notes"]:
        print(f"{n['title']}: {n['content']}")


def search_notes():
    query = prompt("Search in notes: ")
    results = [n for n in data["notes"] if query.lower(
    ) in n["title"].lower() or query.lower() in n["content"].lower()]
    if results:
        for n in results:
            print(f"{n['title']}: {n['content']}")
    else:
        print("No matches found.")


def edit_note():
    title = prompt("Enter note title to edit: ")
    for n in data["notes"]:
        if n["title"].lower() == title.lower():
            new_content = prompt("New content: ")
            n["content"] = new_content
            save_data(data)
            print(f"✏️ Note '{title}' updated.")
            return
    print("Note not found.")


def delete_note():
    title = prompt("Enter note title to delete: ")
    data["notes"] = [n for n in data["notes"]
                     if n["title"].lower() != title.lower()]
    save_data(data)
    print(f"🗑️ Note '{title}' deleted.")


def exit_program():
    print("👋 Goodbye!")
    exit()


"Dictionary of command functions"
COMMAND_FUNCTIONS = {
    'add contact': add_contact,
    'list contacts': list_contacts,
    'search contacts': search_contacts,
    'edit contact': edit_contact,
    'delete contact': delete_contact,
    'birthdays': birthdays,
    'add note': add_note,
    'list notes': list_notes,
    'search notes': search_notes,
    'edit note': edit_note,
    'delete note': delete_note,
    'exit': exit_program
}

"Command suggestion helper"


def suggest_command(user_input):
    user_input = user_input.lower()
    matches = get_close_matches(user_input, COMMANDS.keys(), n=3, cutoff=0.3)
    if matches:
        print("Did you mean:")
        for c in matches:
            print(f" - {c}: {COMMANDS[c]}")
        return matches[0]
    print("❌ Command not recognized.")
    return None


"Main menu loop"


def menu():
    while True:
        try:
            user_input = prompt("Enter command: ", completer=command_completer)
            command = suggest_command(user_input)
            if not command:
                continue
            if command in COMMAND_FUNCTIONS:
                COMMAND_FUNCTIONS[command]()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Exiting gracefully...")
            break


if __name__ == "__main__":
    menu()
