import unittest
import re
from unittest.mock import patch

from src.district_9_personal_assistant.address_book import AddressBook


def strip_ansi(text):
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


questionary_select_path = "src.district_9_personal_assistant.selection.questionary.select"


class TestCoreFlows(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()

    @patch("questionary.text")
    def test_add_contact(self, mock_text):
        mock_text.return_value.ask.return_value = "John Doe"
        result = self.book.add_contact()
        self.assertIn("added", result)
        self.assertEqual(len(self.book.contacts), 1)
        self.assertEqual(self.book.contacts[0].name.value, "John Doe")

    @patch(questionary_select_path)
    def test_select_active_contact(self, mock_select):
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "John Doe"
            self.book.add_contact()
        mock_select.return_value.ask.return_value = "0: John Doe"
        result = self.book.select_active_contact()
        self.assertIn("Active contact set", result)
        self.assertIsNotNone(self.book.get_active_contact())
        self.assertEqual(
            self.book.get_active_contact().name.value,
            "John Doe"
        )

    @patch("questionary.text")
    def test_edit_contact(self, mock_text):
        mock_text.return_value.ask.return_value = "John Doe"
        self.book.add_contact()
        with patch(questionary_select_path) as mock_select:
            mock_select.return_value.ask.return_value = "0: John Doe"
            mock_text.return_value.ask.return_value = "Jane Doe"
            result = self.book.edit_contact()
        self.assertIn("updated", result)
        self.assertEqual(self.book.contacts[0].name.value, "Jane Doe")

    @patch(questionary_select_path)
    def test_delete_contact(self, mock_select):
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "John Doe"
            self.book.add_contact()
        mock_select.return_value.ask.return_value = "0: John Doe"
        result = self.book.delete_contact()
        self.assertIn("removed", result)
        self.assertEqual(len(self.book.contacts), 0)

    def test_show_contacts(self):
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "John Doe"
            self.book.add_contact()
        result = self.book.show_contacts()
        self.assertIn("John Doe", result)

    def test_back_to_book(self):
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "John Doe"
            self.book.add_contact()
        with patch(
            questionary_select_path
        ) as mock_select:
            mock_select.return_value.ask.return_value = "0: John Doe"
            self.book.select_active_contact()
        result = self.book.back_to_book()
        self.assertEqual(strip_ansi(result), "Returned to address book.")
        self.assertIsNone(self.book.get_active_contact())


if __name__ == "__main__":
    unittest.main()
