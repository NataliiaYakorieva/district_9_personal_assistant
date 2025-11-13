import os
from typing import Optional
from .contact import Contact
from .name import Name
from dataclasses import dataclass, field
import questionary
import pickle


@dataclass
class AddressBook:
    """
    Represents an address book containing contacts.
    """
    contacts: list = field(default_factory=list)
    _active_contact: Optional[Contact] = None

    def add_contact(self):
        """Add a new contact to the address book."""
        name_str = questionary.text("Contact name:").ask()
        try:
            name = Name(value=name_str)
            contact = Contact(name=name)
            self.contacts.append(contact)
            return f"Contact {name.value} added."
        except ValueError as e:
            return f"Error adding contact: {e}"

    def find_contact(self):
        """Find a contact by name."""
        name = questionary.text("Contact name:").ask()
        for contact in self.contacts:
            if contact.name.value.lower() == name.lower():
                return contact
        return None

    def select_active_contact(self):
        """Set the active contact for further operations."""
        contact = self.find_contact()
        if contact is None:
            return "Contact not found."
        self._active_contact = contact
        return f"Active contact set to {contact.name.value}."

    def back_to_book(self):
        """Return to the address book (unset active contact)."""
        self._active_contact = None
        return "Returned to address book."

    def get_active_contact(self):
        """Get the currently active contact."""
        return self._active_contact

    def add_phone(self):
        """Add a phone to the active contact."""
        return self._active_contact.add_phone()

    def edit_phone(self):
        """Edit a phone of the active contact."""
        return self._active_contact.edit_phone()

    def delete_phone(self):
        """Delete a phone from the active contact."""
        return self._active_contact.delete_phone()

    def set_main_phone(self):
        """Set a phone as main for the active contact."""
        return self._active_contact.set_main_phone()

    def show_phones(self):
        """Show all phones of the active contact."""
        return self._active_contact.show_phones()

    def reset_main_phone(self):
        """Reset main phone for the active contact."""
        contact = self._active_contact
        contact.reset_main_phone()
        return f"Main phone number reset for contact {contact.name.value}."

    def add_email(self):
        """Add an email to the active contact."""
        return self._active_contact.add_email()

    def edit_email(self):
        """Edit an email of the active contact."""
        return self._active_contact.edit_email()

    def delete_email(self):
        """Delete an email from the active contact."""
        return self._active_contact.delete_email()

    def show_emails(self):
        """Show all emails of the active contact."""
        return self._active_contact.show_emails()

    def set_main_email(self):
        """Set an email as main for the active contact."""
        return self._active_contact.set_main_email()

    def add_note(self):
        """Add a note to the active contact."""
        return self._active_contact.add_note()

    def show_notes(self):
        """Show all notes of the active contact."""
        return self._active_contact.show_notes()

    def edit_note(self):
        """Edit a note of the active contact."""
        return self._active_contact.edit_note()

    def delete_note(self):
        """Delete a note from the active contact."""
        return self._active_contact.delete_note()

    def find_note(self):
        """Find a note of the active contact."""
        return self._active_contact.find_note()

    def find_by_tag(self):
        """Find notes by tag for the active contact."""
        return self._active_contact.find_by_tag()

    def add_address(self):
        """Add an address to the active contact."""
        return self._active_contact.add_address()

    def edit_address(self):
        """Edit an address of the active contact."""
        return self._active_contact.edit_address()

    def delete_address(self):
        """Delete an address from the active contact."""
        return self._active_contact.delete_address()

    def show_addresses(self):
        """Show all addresses of the active contact."""
        return self._active_contact.show_addresses()

    def set_main_address(self):
        """Set an address as main for the active contact."""
        return self._active_contact.set_main_address()

    @staticmethod
    def _get_file_path():
        """Get the file path for saving/loading the address book."""
        home = os.path.expanduser("~")
        return os.path.join(home, "address_book.pkl")

    def save_to_file(self):
        """Save the address book to a file."""
        file_path = self._get_file_path()
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls):
        """Load the address book from a file."""
        file_path = os.path.join(os.path.expanduser("~"), "address_book.pkl")
        try:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()
