import questionary
from src.district_9_personal_assistant.helpers.message import info_message


from src.district_9_personal_assistant.address_book import AddressBook
from src.district_9_personal_assistant.constants.commands import commands_info, Commands
from src.district_9_personal_assistant.helpers.core_utils import (
    parse_input,
    get_commands_list_suggestions,
    get_command_handler,
)
from src.district_9_personal_assistant.helpers.message import success_message, fail_message


def run_personal_assistant():
    book = AddressBook.load_from_file()
    print(info_message("Welcome to the Personal Assistant!"))
    print(commands_info)

    greetings_file = "src/district_9_personal_assistant/constants/greetings.txt"
    birthdays_today = AddressBook.find_birthdays_this_day(book.contacts, greetings_file)
    if birthdays_today:
        print(success_message(f"\n🎉 Today's birthdays: {', '.join(birthdays_today.keys())}"))

    while True:
        active_contact = book.get_active_contact()
        commands_list = get_commands_list_suggestions(active_contact)

        if active_contact is not None:
            print(info_message(f"Working on the contact: {active_contact.name}"))

        user_input = questionary.autocomplete(
            "Enter a command:",
            choices=commands_list,
            match_middle=True,
        ).ask()

        command = parse_input(user_input)
        if command is None:
            print(fail_message("Invalid command input."))
            continue

        handler_map = get_command_handler(book)
        handler = handler_map.get(command)
        if handler is None:
            print(fail_message("Unknown command. Type 'help' to see available commands."))
            continue

        result = handler()

        if result is not None:
            print(result)

        if command == Commands.EXIT.value:
            break
