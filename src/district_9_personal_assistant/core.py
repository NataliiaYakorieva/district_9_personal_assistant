from .address_book import AddressBook
import questionary
from .constants.commands import book_commands_list, contact_commands_list, commands_info, Commands
from .message import fail_message, success_message


def input_error(func):
    """
    Decorator for handling input errors and displaying informative messages.
    Now also handles AttributeError for missing contacts.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return fail_message("Error: Contact not found")
        except (KeyError, ValueError, IndexError) as e:
            return fail_message(f"Error: {str(e)}")
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


def run_personal_assistant():
    book = AddressBook.load_from_file()
    print("Welcome to the Personal Assistant!")
    print(commands_info)

    while True:
        active_contact = book.get_active_contact()
        commands_list = get_current_commands_list(active_contact)

        if active_contact is not None:
            print(success_message(f"Working on the contact: {active_contact.name}"))

        user_input = questionary.autocomplete(
            "Enter a command:",
            choices=commands_list,
            match_middle=True,
        ).ask()

        command, *args = parse_input(user_input)

        def handle_help():
            print(success_message(f"{commands_info}\n"))

        def handle_exit():
            book.save_to_file()
            print(success_message("Exit. Data saved."))

        if active_contact is None:
            match command:
                case Commands.ADD_CONTACT.value:
                    print(book.add_contact())
                case Commands.FIND_CONTACT.value:
                    print(book.find_contact())
                case Commands.HELP.value:
                    handle_help()
                case Commands.SELECT_ACTIVE_CONTACT.value:
                    print(book.select_active_contact())
                case Commands.EDIT_CONTACT.value:
                    print(book.edit_contact())
                case Commands.DELETE_CONTACT.value:
                    print(book.delete_contact())
                case Commands.SHOW_CONTACTS.value:
                    print(book.show_contacts())
                case Commands.EXIT.value:
                    handle_exit()
                    break
                case _:
                    print(fail_message("Unknown command."))
        else:
            match command:
                case Commands.ADD_PHONE.value:
                    print(book.add_phone())
                case Commands.EDIT_PHONE.value:
                    print(book.edit_phone())
                case Commands.DELETE_PHONE.value:
                    print(book.delete_phone())
                case Commands.SHOW_PHONES.value:
                    print(book.show_phones())
                case Commands.SET_MAIN_PHONE.value:
                    print(book.set_main_phone())
                case Commands.ADD_EMAIL.value:
                    print(book.add_email())
                case Commands.EDIT_EMAIL.value:
                    print(book.edit_email())
                case Commands.DELETE_EMAIL.value:
                    print(book.delete_email())
                case Commands.SHOW_EMAILS.value:
                    print(book.show_emails())
                case Commands.SET_MAIN_EMAIL.value:
                    print(book.set_main_email())
                case Commands.ADD_NOTE.value:
                    print(book.add_note())
                case Commands.EDIT_NOTE.value:
                    print(book.edit_note())
                case Commands.DELETE_NOTE.value:
                    print(book.delete_note())
                case Commands.SHOW_NOTES.value:
                    print(book.show_notes())
                case Commands.FIND_NOTE.value:
                    print(book.find_note())
                case Commands.FIND_BY_TAG.value:
                    print(book.find_by_tag())
                case Commands.ADD_ADDRESS.value:
                    print(book.add_address())
                case Commands.EDIT_ADDRESS.value:
                    print(book.edit_address())
                case Commands.DELETE_ADDRESS.value:
                    print(book.delete_address())
                case Commands.SHOW_ADDRESSES.value:
                    print(book.show_addresses())
                case Commands.SET_MAIN_ADDRESS.value:
                    print(book.set_main_address())
                case Commands.EXIT.value:
                    handle_exit()
                    break
                case Commands.HELP.value:
                    handle_help()
                case Commands.BACK_TO_BOOK.value:
                    print(book.back_to_book())
                case _:
                    print(fail_message("Unknown command."))
