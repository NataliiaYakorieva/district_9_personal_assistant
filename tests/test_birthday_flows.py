import unittest
from unittest.mock import patch
from datetime import date

from src.district_9_personal_assistant.address_book import AddressBook


class TestBirthdayBookFlows(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "John Doe"
            self.book.add_contact()
        with patch(
            "src.district_9_personal_assistant.selection.questionary.select"
        ) as mock_select:
            mock_select.return_value.ask.return_value = "0: John Doe"
            self.book.select_active_contact()

    @patch("questionary.text")
    def test_add_birthday(self, mock_text):
        mock_text.return_value.ask.return_value = "01.01.2000"
        result = self.book._active_contact.add_birthday()
        self.assertIn("Birthday set to", result)
        self.assertIsNotNone(self.book._active_contact.birthday)
        self.assertEqual(
            self.book._active_contact.birthday.birthday.strftime("%d.%m.%Y"),
            "01.01.2000")

    def test_find_birthdays_this_week(self):
        with patch("questionary.text") as mock_text:
            today = date.today()
            bday_str = today.strftime("%d.%m.%Y")
            mock_text.return_value.ask.return_value = bday_str
            self.book._active_contact.add_birthday()
        result = AddressBook.find_birthdays_this_week(self.book.contacts)
        self.assertIn(self.book._active_contact.name.value, result)
        self.assertIsInstance(result[self.book._active_contact.name.value], date)

    @patch("questionary.confirm")
    def test_find_birthdays_this_day(self, mock_confirm):
        with patch("questionary.text") as mock_text:
            today = date.today()
            bday_str = today.strftime("%d.%m.%Y")
            mock_text.return_value.ask.return_value = bday_str
            self.book._active_contact.add_birthday()
        mock_confirm.return_value.ask.return_value = False
        result = AddressBook.find_birthdays_this_day(self.book.contacts)
        self.assertIn(self.book._active_contact.name.value, result)
        self.assertEqual(result[self.book._active_contact.name.value], today)


if __name__ == "__main__":
    unittest.main()
