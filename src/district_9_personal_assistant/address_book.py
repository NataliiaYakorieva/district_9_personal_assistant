import os
import random
from typing import Optional
from datetime import date, timedelta
from dataclasses import dataclass, field

import questionary
import pickle

from src.district_9_personal_assistant.contact import Contact
from src.district_9_personal_assistant.name import Name
from src.district_9_personal_assistant.selection import Selection
from src.district_9_personal_assistant.helpers.message import fail_message, success_message


@dataclass
class AddressBook(Selection):
    """
    Represents an address book containing contacts.
    """
    contacts: list = field(default_factory=list)
    _active_contact: Optional[Contact] = None

    def add_contact(self) -> str:
        """
        Add a new contact to the address book.
        Returns a success or failure message.
        """
        name_str = questionary.text("Contact name:").ask()
        if any(contact.name.value.lower() == name_str.lower() for contact in self.contacts):
            return fail_message(
                "Contact with this name already exists. "
                "Please enter a different name."
            )
        try:
            name = Name(value=name_str)
            contact = Contact(name=name)
            self.contacts.append(contact)
            return success_message(f"Contact {name.value} added.")
        except ValueError as e:
            return fail_message(f"Error adding contact: {e}")

    def find_contact(self, used_for_selection: bool = False) -> Optional[Contact]:
        """
        Find a contact by name or by interactive selection.
        Returns the selected Contact or None.
        """
        if not used_for_selection and not self.contacts:
            return fail_message("No contacts found.")
        return self.select_item_interactively(
            self.contacts,
            lambda c: c.name.value,
            "Select contact:"
        )

    def select_active_contact(self) -> str:
        """
        Set the active contact for further operations using interactive selection.
        Returns a success or failure message.
        """
        contact = self.select_item_interactively(
            self.contacts,
            lambda c: c.name.value,
            "Select contact:",
        )
        if contact is None:
            return fail_message("Contact not found.")
        self._active_contact = contact
        return success_message(f"Active contact set to {contact.name.value}.")

    def back_to_book(self) -> str:
        """
        Return to the address book (unset active contact).
        Returns a success message.
        """
        self._active_contact = None
        return success_message("Returned to address book.")

    def get_active_contact(self) -> Optional[Contact]:
        """
        Get the currently active contact.
        Returns the active Contact or None.
        """
        return self._active_contact

    def add_phone(self) -> str:
        """
        Add a phone to the active contact.
        """
        return self._active_contact.add_phone()

    def edit_phone(self) -> str:
        """
        Edit a phone of the active contact.
        """
        return self._active_contact.edit_phone()

    def delete_phone(self) -> str:
        """
        Delete a phone from the active contact.
        """
        return self._active_contact.delete_phone()

    def set_main_phone(self) -> str:
        """
        Set a phone as main for the active contact.
        """
        return self._active_contact.set_main_phone()

    def show_phones(self) -> str:
        """
        Show all phones of the active contact.
        """
        return self._active_contact.show_phones()

    def add_email(self) -> str:
        """
        Add an email to the active contact.
        """
        return self._active_contact.add_email()

    def edit_email(self) -> str:
        """
        Edit an email of the active contact.
        """
        return self._active_contact.edit_email()

    def delete_email(self) -> str:
        """
        Delete an email from the active contact.
        """
        return self._active_contact.delete_email()

    def show_emails(self) -> str:
        """
        Show all emails of the active contact.
        """
        return self._active_contact.show_emails()

    def set_main_email(self) -> str:
        """
        Set an email as main for the active contact.
        """
        return self._active_contact.set_main_email()

    def add_note(self) -> str:
        """
        Add a note to the active contact.
        """
        return self._active_contact.add_note()

    def show_notes(self) -> str:
        """
        Show all notes of the active contact.
        """
        return self._active_contact.show_notes()

    def edit_note(self) -> str:
        """
        Edit a note of the active contact.
        """
        return self._active_contact.edit_note()

    def delete_note(self) -> str:
        """
        Delete a note from the active contact.
        """
        return self._active_contact.delete_note()

    def find_note(self) -> str:
        """
        Find a note of the active contact.
        """
        return self._active_contact.find_note()

    def find_by_tag(self) -> str:
        """
        Find notes by tag for the active contact.
        """
        return self._active_contact.find_by_tag()

    def add_address(self) -> str:
        """
        Add an address to the active contact.
        """
        return self._active_contact.add_address()

    def edit_address(self) -> str:
        """
        Edit an address of the active contact.
        """
        return self._active_contact.edit_address()

    def delete_address(self) -> str:
        """
        Delete an address from the active contact.
        """
        return self._active_contact.delete_address()

    def show_addresses(self) -> str:
        """
        Show all addresses of the active contact.
        """
        return self._active_contact.show_addresses()

    def set_main_address(self) -> str:
        """
        Set an address as main for the active contact.
        """
        return self._active_contact.set_main_address()

    def add_birthday(self) -> str:
        """
        Add a birthday to the active contact.
        """
        return self._active_contact.add_birthday()

    def show_birthday(self) -> str:
        """
        Show the birthday of the active contact.
        """
        return self._active_contact.show_birthday()

    def edit_contact(self) -> str:
        """
        Edit the name of an existing contact.
        """
        contact = self.find_contact(True)
        if contact is None:
            return fail_message("No contacts found.")
        new_name = questionary.text("Enter new name for:", default=contact.name.value).ask()
        if not new_name:
            return fail_message("No new name provided.")
        if any(c.name.value.lower() == new_name.lower() for c in self.contacts if c != contact):
            return fail_message("Another contact with this name already exists.")
        contact.name.value = new_name
        return success_message(f"Contact name updated to {new_name}.")

    def delete_contact(self) -> str:
        """
        Remove a contact from the address book.
        """
        contact = self.find_contact(True)
        if contact is None:
            return fail_message("No contacts found.")
        self.contacts.remove(contact)
        if self._active_contact == contact:
            self._active_contact = None
        return success_message(f"Contact {contact.name.value} removed.")

    def show_contacts(self) -> str:
        """
        Show all contacts in the address book.
        """
        if not self.contacts:
            return fail_message("No contacts found.")
        return "\n".join(
            f"{idx + 1}. {contact.name.value}"
            for idx, contact in enumerate(self.contacts)
        )

    def open_in_google_maps(self) -> None:
        """
        Open the main address of the active contact on Google Maps.
        """
        return self._active_contact.open_in_google_maps()

    def show_birthdays_this_week(self) -> str:
        """
        Find and display all contacts with birthdays this week.
        """
        birthdays = self.find_birthdays_this_week(self.contacts)
        if not birthdays:
            return fail_message("No birthdays this week.")

        result = ["Birthdays this week:"]
        for name, bday_date in birthdays.items():
            result.append(f"  {name}: {bday_date.strftime('%d.%m.%Y')}")
        return success_message("\n".join(result))

    @staticmethod
    def _get_file_path() -> str:
        """
        Get the file path for saving/loading the address book.
        """
        home = os.path.expanduser("~")
        return os.path.join(home, "address_book.pkl")

    def save_to_file(self) -> None:
        """
        Save the address book to a file.
        """
        file_path = self._get_file_path()
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls) -> "AddressBook":
        """
        Load the address book from a file.
        """
        file_path = os.path.join(os.path.expanduser("~"), "address_book.pkl")
        try:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()

    @classmethod
    def find_birthdays_this_week(cls, contacts: list) -> dict[str, date]:
        """
        Find contacts with birthdays this week.
        Returns a dictionary mapping contact names to birthday dates.
        """
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        birthdays_this_week = {}

        for contact in contacts:
            bday = getattr(contact, "birthday", None)
            name = getattr(contact, "name", None)
            if bday and bday.birthday:
                next_bday = bday.birthday.replace(year=today.year)
                if next_bday < today:
                    next_bday = bday.birthday.replace(year=today.year + 1)
                if start_of_week <= next_bday <= end_of_week:
                    birthdays_this_week[name.value] = next_bday

        return birthdays_this_week

    @classmethod
    def find_birthdays_this_day(
            cls, contacts: list, filepath: str = "greetings.txt") -> dict[str, date]:
        """
        Find contacts with birthdays today and optionally suggest greetings.
        Returns a dictionary mapping contact names to today's date.
        """
        today = date.today()
        birthdays_today = {}

        for contact in contacts:
            bday = getattr(contact, "birthday", None)
            name = getattr(contact, "name", None)
            if bday and bday.birthday:
                today_bday = bday.birthday.replace(year=today.year)
                if today_bday == today:
                    birthdays_today[name.value] = today_bday

                    greetings_sug = questionary.confirm(
                        f"Do you want me to suggest some greetings for {name.value}?"
                    ).ask()
                    if greetings_sug:
                        try:
                            with open(filepath, "r", encoding="utf-8") as file:
                                greetings = [line.strip() for line in file if line.strip()]
                            if not greetings:
                                print("File is empty.")
                                continue
                            for i, greeting in enumerate(
                                random.sample(greetings, min(3, len(greetings))), 1
                            ):
                                print(f"{i}. {greeting.replace('{name}', name.value)}")
                        except Exception as e:
                            print(f"Error reading greetings file: {e}")
                    else:
                        continue

        return birthdays_today
