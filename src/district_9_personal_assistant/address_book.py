from .contact import Contact
from dataclasses import dataclass, field


@dataclass
class AddressBook:
    contacts: list = field(default_factory=list)

    def add_contact(self):
        name = input("Contact name: ")
        contact = Contact(name=name)
        self.contacts.append(contact)
        return f"Contact {name} added."

    def find_contact(self):
        name = input("Contact name: ")
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None

    @staticmethod
    def require_contact(func):
        def wrapper(self, *args, **kwargs):
            contact = self.find_contact()
            if contact is None:
                return "Contact not found."
            return func(self, contact, *args, **kwargs)
        return wrapper

    @require_contact
    def show_notes(self, contact):
        return contact.show_notes()

    @require_contact
    def add_note(self, contact):
        return contact.add_note()

    @require_contact
    def edit_note(self, contact):
        return contact.edit_note()

    @require_contact
    def delete_note(self, contact):
        return contact.delete_note()

    @require_contact
    def list_notes(self, contact):
        if not hasattr(contact, "notes") or not contact.notes:
            return "No notes found."
        return "\n".join(str(note) for note in contact.notes)
