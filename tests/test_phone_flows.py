import unittest
from unittest.mock import patch

from src.district_9_personal_assistant.address_book import AddressBook


class TestPhoneBookFlows(unittest.TestCase):
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
    @patch("questionary.confirm")
    def test_add_phone(self, mock_confirm, mock_text):
        mock_text.return_value.ask.return_value = "+4912345678901"
        mock_confirm.return_value.ask.return_value = True
        result = self.book.add_phone()
        self.assertIn("added to contact", result)
        self.assertTrue(len(self.book._active_contact.phones) == 1)

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    @patch("questionary.text")
    def test_edit_phone(self, mock_text, mock_select):
        with patch("questionary.text") as add_text, patch("questionary.confirm") as add_confirm:
            add_text.return_value.ask.return_value = "+4912345678901"
            add_confirm.return_value.ask.return_value = True
            self.book.add_phone()

        mock_select.return_value.ask.return_value = "0: +4912345678901"
        mock_text.return_value.ask.return_value = "+4912345678902"
        result = self.book.edit_phone()
        self.assertIn("updated", result)
        phone = self.book._active_contact.phones[0]
        self.assertEqual(phone.number, "+4912345678902")

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    def test_delete_phone(self, mock_select):
        with patch("questionary.text") as add_text, patch("questionary.confirm") as add_confirm:
            add_text.return_value.ask.return_value = "+4912345678901"
            add_confirm.return_value.ask.return_value = True
            self.book.add_phone()

        mock_select.return_value.ask.return_value = "0: +4912345678901"
        result = self.book.delete_phone()
        self.assertIn("deleted", result)
        self.assertEqual(len(self.book._active_contact.phones), 0)

    def test_show_phones(self):
        with patch("questionary.text") as mock_text, patch("questionary.confirm") as mock_confirm:
            mock_text.return_value.ask.return_value = "+4912345678901"
            mock_confirm.return_value.ask.return_value = True
            self.book.add_phone()
        result = self.book.show_phones()
        self.assertIn("+4912345678901", result)

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    def test_set_main_phone(self, mock_select):
        with patch("questionary.text") as mock_text, patch("questionary.confirm") as mock_confirm:
            mock_text.return_value.ask.return_value = "+4912345678901"
            mock_confirm.return_value.ask.return_value = False
            self.book.add_phone()
            mock_text.return_value.ask.return_value = "+4912345678902"
            mock_confirm.return_value.ask.return_value = False
            self.book.add_phone()

        mock_select.return_value.ask.return_value = "1: +4912345678902"
        result = self.book.set_main_phone()
        self.assertIn("Main number is set", result)
        phones = self.book._active_contact.phones
        self.assertTrue(phones[1].is_main)
        self.assertFalse(phones[0].is_main)


if __name__ == "__main__":
    unittest.main()
