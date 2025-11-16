from src.district_9_personal_assistant.address_book import AddressBook
from src.district_9_personal_assistant.constants.commands import (
    book_commands_list,
    contact_commands_list,
    Commands,
    commands_info,
)
from src.district_9_personal_assistant.helpers.message import success_message


def parse_input(user_input: str) -> str | None:
    """
    Parses the user's input command.
    Returns only the command (ignores any arguments).

    Args:
        user_input: The raw input string from the user.

    Returns:
        The command string, or None if input is invalid.
    """
    if not isinstance(user_input, str) or not user_input.strip():
        return None
    parts = user_input.split()
    if not parts:
        return None
    cmd = parts[0].strip().lower()
    return cmd


def get_commands_list_suggestions(active_contact) -> list:
    """
    Get the list of command suggestions based on whether a contact is active.

    Args:
        active_contact: The currently active contact or None.

    Returns:
        List of command strings.
    """
    if active_contact is None:
        return book_commands_list
    else:
        return contact_commands_list


def handle_help() -> None:
    """
    Print the commands info/help to the console.
    """
    print(f"{commands_info}\n")


def handle_exit(book: AddressBook) -> None:
    """
    Save the address book and print exit message.

    Args:
        book: The AddressBook instance to save.
    """
    book.save_to_file()
    print(success_message("Exit. Data saved."))


def get_command_handler(book: AddressBook) -> dict:
    """
    Get a mapping of command strings to handler functions for the current context.

    Args:
        book: The AddressBook instance.

    Returns:
        Dictionary mapping command strings to handler functions.
    """
    active_contact = book.get_active_contact()
    if active_contact is None:
        return {
            Commands.ADD_CONTACT.value: book.add_contact,
            Commands.FIND_CONTACT.value: book.find_contact,
            Commands.SELECT_ACTIVE_CONTACT.value: book.select_active_contact,
            Commands.EDIT_CONTACT.value: book.edit_contact,
            Commands.DELETE_CONTACT.value: book.delete_contact,
            Commands.SHOW_CONTACTS.value: book.show_contacts,
            Commands.FIND_BIRTHDAYS_THIS_WEEK.value: book.show_birthdays_this_week,
            Commands.EXIT.value: lambda: handle_exit(book),
            Commands.HELP.value: handle_help,
        }

    return {
        # phone commands
        Commands.ADD_PHONE.value: book.add_phone,
        Commands.EDIT_PHONE.value: book.edit_phone,
        Commands.DELETE_PHONE.value: book.delete_phone,
        Commands.SHOW_PHONES.value: book.show_phones,
        Commands.SET_MAIN_PHONE.value: book.set_main_phone,
        # email commands
        Commands.ADD_EMAIL.value: book.add_email,
        Commands.EDIT_EMAIL.value: book.edit_email,
        Commands.DELETE_EMAIL.value: book.delete_email,
        Commands.SHOW_EMAILS.value: book.show_emails,
        Commands.SET_MAIN_EMAIL.value: book.set_main_email,
        # note commands
        Commands.ADD_NOTE.value: book.add_note,
        Commands.EDIT_NOTE.value: book.edit_note,
        Commands.DELETE_NOTE.value: book.delete_note,
        Commands.SHOW_NOTES.value: book.show_notes,
        Commands.FIND_NOTE.value: book.find_note,
        Commands.FIND_BY_TAG.value: book.find_by_tag,
        # address commands
        Commands.ADD_ADDRESS.value: book.add_address,
        Commands.EDIT_ADDRESS.value: book.edit_address,
        Commands.DELETE_ADDRESS.value: book.delete_address,
        Commands.SHOW_ADDRESSES.value: book.show_addresses,
        Commands.SET_MAIN_ADDRESS.value: book.set_main_address,
        Commands.OPEN_IN_GOOGLE_MAPS.value: book.open_in_google_maps,
        # birthday commands
        Commands.ADD_BIRTHDAY.value: book.add_birthday,
        Commands.SHOW_BIRTHDAY.value: book.show_birthday,
        # other commands
        Commands.EXIT.value: lambda: handle_exit(book),
        Commands.HELP.value: handle_help,
        Commands.BACK_TO_BOOK.value: book.back_to_book,
    }
