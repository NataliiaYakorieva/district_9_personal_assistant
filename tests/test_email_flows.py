import unittest
from unittest.mock import patch
from src.district_9_personal_assistant.address_book import AddressBook


class TestEmailBookFlows(unittest.TestCase):
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
    def test_add_email(self, mock_text):
        mock_text.return_value.ask.return_value = "john.doe@example.com"
        result = self.book.add_email()
        self.assertIn("added to contact", result)
        self.assertTrue(len(self.book.get_active_contact().emails) == 1)
        self.assertEqual(self.book.get_active_contact().emails[0].address, "john.doe@example.com")

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    @patch("questionary.text")
    def test_edit_email(self, mock_text, mock_select):
        with patch("questionary.text") as add_text:
            add_text.return_value.ask.return_value = "john.doe@example.com"
            self.book.add_email()
        mock_select.return_value.ask.return_value = "0: john.doe@example.com"
        mock_text.return_value.ask.return_value = "jane.doe@example.com"
        result = self.book.edit_email()
        self.assertIn("updated", result)
        email = self.book.get_active_contact().emails[0]
        self.assertEqual(email.address, "jane.doe@example.com")

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    def test_delete_email(self, mock_select):
        with patch("questionary.text") as add_text:
            add_text.return_value.ask.return_value = "john.doe@example.com"
            self.book.add_email()
        mock_select.return_value.ask.return_value = "0: john.doe@example.com"
        result = self.book.delete_email()
        self.assertIn("deleted", result)
        self.assertEqual(len(self.book.get_active_contact().emails), 0)

    def test_show_emails(self):
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "john.doe@example.com"
            self.book.add_email()
        result = self.book.show_emails()
        self.assertIn("john.doe@example.com", result)

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    def test_set_main_email(self, mock_select):
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "john.doe@example.com"
            self.book.add_email()
            mock_text.return_value.ask.return_value = "jane.doe@example.com"
            self.book.add_email()
        mock_select.return_value.ask.return_value = "1: jane.doe@example.com"
        result = self.book.set_main_email()
        emails = self.book.get_active_contact().emails
        self.assertIn("Main email set", result)
        self.assertTrue(emails[1].is_main)
        self.assertFalse(getattr(emails[0], "is_main", False))


if __name__ == "__main__":
    unittest.main()
