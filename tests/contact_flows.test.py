import unittest
import re
from unittest.mock import patch
from src.district_9_personal_assistant.address_book import AddressBook


def strip_ansi(text):
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


questionary_select_path = "src.district_9_personal_assistant.selection.questionary.select"


class TestContactBookFlows(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "John Doe"
            self.book.add_contact()
        with patch(questionary_select_path) as mock_select:
            mock_select.return_value.ask.return_value = "0: John Doe"
            self.book.select_active_contact()

    @patch(questionary_select_path)
    @patch("questionary.text")
    def test_edit_contact(self, mock_text, mock_select):
        mock_select.return_value.ask.return_value = "0: John Doe"
        mock_text.return_value.ask.return_value = "Jane Doe"
        result = self.book.edit_contact()
        self.assertIn("updated", result)
        self.assertEqual(self.book.get_active_contact().name.value, "Jane Doe")

    @patch(questionary_select_path)
    def test_delete_contact(self, mock_select):
        mock_select.return_value.ask.return_value = "0: John Doe"
        result = self.book.delete_contact()
        self.assertIn("removed", result)
        self.assertEqual(len(self.book.contacts), 0)
        self.assertIsNone(self.book.get_active_contact())

    def test_show_contacts(self):
        result = self.book.show_contacts()
        self.assertIn("John Doe", result)

    @patch("questionary.text")
    def test_add_birthday(self, mock_text):
        mock_text.return_value.ask.return_value = "01.01.2000"
        result = self.book.get_active_contact().add_birthday()
        self.assertIn("Birthday set to", result)
        self.assertIsNotNone(self.book.get_active_contact().birthday)

    def test_back_to_book(self):
        result = self.book.back_to_book()
        self.assertEqual(strip_ansi(result), "Returned to address book.")
        self.assertIsNone(self.book.get_active_contact())

    def test_get_active_contact(self):
        contact = self.book.get_active_contact()
        self.assertIsNotNone(contact)
        self.assertEqual(contact.name.value, "John Doe")


if __name__ == "__main__":
    unittest.main()
