from enum import Enum


class Commands(Enum):
    # shared commands
    EXIT = "exit"
    HELP = "help"

    # book commands
    ADD_CONTACT = "add_contact"
    FIND_CONTACT = "find_contact"
    SELECT_ACTIVE_CONTACT = "select_active_contact"
    BACK_TO_BOOK = "back_to_book"

    # phone
    ADD_PHONE = "add_phone"
    EDIT_PHONE = "edit_phone"
    DELETE_PHONE = "delete_phone"
    SHOW_PHONES = "show_phones"
    SET_MAIN_PHONE = "set_main_phone"

    # email
    ADD_EMAIL = "add_email"
    EDIT_EMAIL = "edit_email"
    DELETE_EMAIL = "delete_email"
    SHOW_EMAILS = "show_emails"
    SET_MAIN_EMAIL = "set_main_email"

    # note
    ADD_NOTE = "add_note"
    EDIT_NOTE = "edit_note"
    DELETE_NOTE = "delete_note"
    SHOW_NOTES = "show_notes"
    FIND_NOTE = "find_note"
    FIND_BY_TAG = "find_by_tag"

    # address
    ADD_ADDRESS = "add_address"
    EDIT_ADDRESS = "edit_address"
    DELETE_ADDRESS = "delete_address"
    SHOW_ADDRESSES = "show_addresses"
    SET_MAIN_ADDRESS = "set_main_address"


book_commands_list = [
    Commands.ADD_CONTACT.value,
    Commands.FIND_CONTACT.value,
    Commands.SELECT_ACTIVE_CONTACT.value,
    Commands.EXIT.value,
    Commands.HELP.value
]

contact_commands_list = [
    # phone
    Commands.ADD_PHONE.value,
    Commands.EDIT_PHONE.value,
    Commands.DELETE_PHONE.value,
    Commands.SHOW_PHONES.value,
    Commands.SET_MAIN_PHONE.value,
    # email
    Commands.ADD_EMAIL.value,
    Commands.EDIT_EMAIL.value,
    Commands.DELETE_EMAIL.value,
    Commands.SHOW_EMAILS.value,
    Commands.SET_MAIN_EMAIL.value,
    # note
    Commands.ADD_NOTE.value,
    Commands.EDIT_NOTE.value,
    Commands.DELETE_NOTE.value,
    Commands.SHOW_NOTES.value,
    Commands.FIND_NOTE.value,
    Commands.FIND_BY_TAG.value,
    # address
    Commands.ADD_ADDRESS.value,
    Commands.EDIT_ADDRESS.value,
    Commands.DELETE_ADDRESS.value,
    Commands.SHOW_ADDRESSES.value,
    Commands.SET_MAIN_ADDRESS.value,
    # shared
    Commands.EXIT.value,
    Commands.HELP.value,
    Commands.BACK_TO_BOOK.value
]

commands_info = (
    "\nAvailable commands:\n"
    "  add_contact\n"
    "    - name (required): Name of the contact\n"
    "  find_contact\n"
    "    - name (required): Name of the contact to find\n"
    "  add_phone\n"
    "    - contact name (required): Name of the contact to add a phone number to\n"
    "    - phone (required): Phone number to add\n"
    "  edit_phone\n"
    "    - contact name (required): Name of the contact whose phone to edit\n"
    "    - phone (required): Phone number to edit\n"
    "  delete_phone\n"
    "    - contact name (required): Name of the contact whose phone to delete\n"
    "    - phone (required): Phone number to delete\n"
    "  show_phones\n"
    "    - contact name (required): Name of the contact whose phone numbers to list\n"
    "  set_main_phone\n"
    "    - contact name (required): Name of the contact to set the main phone number\n"
    "  add_email\n"
    "    - contact name (required): Name of the contact to add an email to\n"
    "    - email (required): Email address to add\n"
    "  edit_email\n"
    "    - contact name (required): Name of the contact whose email to edit\n"
    "    - old email (required): Existing email address to replace\n"
    "    - new email (required): New email address\n"
    "  delete_email\n"
    "    - contact name (required): Name of the contact whose email to delete\n"
    "    - email (required): Email address to delete\n"
    "  show_emails\n"
    "    - contact name (required): Name of the contact whose emails to list\n"
    "  set_main_email\n"
    "    - contact name (required): Name of the contact to set the main email\n"
    "  add_note\n"
    "    - contact name (required): Name of the contact to add a note to\n"
    "    - title (optional): Brief subject line for the note\n"
    "    - text (required): Content of the note\n"
    "    - tags (optional): Comma-separated tags (e.g., meeting, follow-up)\n"
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
    "  show_notes\n"
    "    - contact name (required): Name of the contact whose notes to list\n"
    "  find_note\n"
    "    - contact name (required): Name of the contact whose notes to search\n"
    "    - query (required): Search by text, tag, or title\n"
    "  find_by_tag\n"
    "    - contact name (required): Name of the contact whose notes to search\n"
    "    - tag (required): Tag to search for\n"
    "  add_address\n"
    "    - contact name (required): Name of the contact to add an address to\n"
    "    - country, city, street_address, zip_code (required)\n"
    "  edit_address\n"
    "    - contact name (required): Name of the contact whose address to edit\n"
    "    - address (required): Address to edit\n"
    "  delete_address\n"
    "    - contact name (required): Name of the contact whose address to delete\n"
    "    - address (required): Address to delete\n"
    "  show_addresses\n"
    "    - contact name (required): Name of the contact whose addresses to list\n"
    "  set_main_address\n"
    "    - contact name (required): Name of the contact to set the main address\n"
    "  exit\n"
    "    - Exit and save data\n")
