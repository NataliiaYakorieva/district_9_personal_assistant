from .address_book import AddressBook

commands_info = (
    "\nAvailable commands:\n"
    "  add_contact\n"
    "    - name (required): Name of the contact\n"
    "  find_contact\n"
    "    - name (required): Name of the contact to find\n"
    "  add_phone\n"
    "    - contact name (required): Name of the contact to add a" +
    "phone number to\n"
    "    - phone (required): Phone number to add\n"
    "  show_phones\n"
    "    - contact name (required): Name of the contact whose phone" +
    "numbers to list\n"
    "  reset_main_phone\n"
    "    - contact name (required): Name of the contact to reset the" +
    "main phone number\n"
    "    - phone (required): Phone number to set as the main phone\n"
    "  add_email\n"
    "    - contact name (required): Name of the contact to add an email to\n"
    "    - email (required): Email address to add\n"
    "  change_email\n"
    "    - contact name (required): Name of the contact whose email" +
    "to change\n"
    "    - old email (required): Existing email address to replace\n"
    "    - new email (required): New email address\n"
    "  remove_email\n"
    "    - contact name (required): Name of the contact whose " +
    "email to remove\n"
    "    - email (required): Email address to remove\n"
    "  add_note\n"
    "    - contact name (required): Name of the contact to add a note to\n"
    "    - title (optional): Brief subject line for the note\n"
    "    - text (required): Content of the note\n"
    "    - tags (optional): Comma-separated tags (e.g., meeting, follow-up)\n"
    "  show_notes\n"
    "    - contact name (required): Name of the contact whose notes to list\n"
    "  edit_note\n"
    "    - contact name (required): Name of the contact whose note to edit\n"
    "    - query (required): Search by text, tag, or title to find the note\n"
    "    - index (required if multiple matches): Note index to edit\n"
    "    - content (optional): New content\n"
    "    - tags (optional): New tags (comma separated)\n"
    "  delete_note\n"
    "    - contact name (required): Name of the contact whose note to delete\n"
    "    - query (required): Search by text, tag, or title to find the note\n"
    "    - index (required if multiple matches): Note index to delete\n"
    "  exit\n"
    "    - Exit and save data\n")


def input_error(func):
    """
    Decorator for handling input errors and displaying informative messages.
    Now also handles AttributeError for missing contacts.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return "Error: Contact not found"
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper


@input_error
def parse_input(user_input):
    """
    Parses the user's input command.
    Returns the command and a list of arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def run_personal_assistant():
    book = AddressBook()
    print("Welcome to the Personal Assistant!\n")
    print(f"{commands_info}\n")

    while True:

        user_input = input("Enter a command: ")
        # TODO We should use ARGS
        command, *args = parse_input(user_input)

        match command:
            case "add_contact":
                print(book.add_contact())
            case "find_contact":
                print(book.find_contact())
            case "add_phone":
                print(book.add_phone())
            case "show_phones":
                print(book.show_phones())
            case "set_main_phone":
                print(book.set_main_phone())
            case "reset_main_phone":
                print(book.reset_main_phone())
            case "add_email":
                print(book.add_email())
            case "change_email":
                print(book.change_email())
            case "remove_email":
                print(book.remove_email())
            case "add_note":
                print(book.add_note())
            case "list_notes":
                print(book.list_notes())
            case "edit_note":
                print(book.edit_note())
            case "delete_note":
                print(book.delete_note())
            case "exit":
                print("Exit. Data saved.")
                break
            case "help":
                print(f"{commands_info}\n")
            case _:
                print("Unknown command.")
