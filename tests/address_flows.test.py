import unittest
from unittest.mock import patch
from src.district_9_personal_assistant.address_book import AddressBook


class TestAddressBookAddressFlows(unittest.TestCase):
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
    def test_add_address(self, mock_text):
        mock_text.side_effect = [
            unittest.mock.Mock(ask=lambda: "Germany"),
            unittest.mock.Mock(ask=lambda: "Berlin"),
            unittest.mock.Mock(ask=lambda: "Main St"),
            unittest.mock.Mock(ask=lambda: "12345"),
        ]
        result = self.book.add_address()
        self.assertIn("added to contact", result)
        self.assertTrue(len(self.book._active_contact.addresses) == 1)

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    @patch("questionary.text")
    def test_edit_address(self, mock_text, mock_select):
        mock_text.side_effect = [
            unittest.mock.Mock(ask=lambda: "Germany"),
            unittest.mock.Mock(ask=lambda: "Berlin"),
            unittest.mock.Mock(ask=lambda: "Main St"),
            unittest.mock.Mock(ask=lambda: "12345"),
        ]
        self.book.add_address()
        mock_select.return_value.ask.return_value = "0: Germany, Berlin, 12345, GERMANY"
        mock_text.side_effect = [
            unittest.mock.Mock(ask=lambda: "France"),
            unittest.mock.Mock(ask=lambda: "Paris"),
            unittest.mock.Mock(ask=lambda: "Rue de Main"),
            unittest.mock.Mock(ask=lambda: "54321"),
        ]
        result = self.book.edit_address()
        addr = self.book._active_contact.addresses[0]
        self.assertIn("updated", result)
        self.assertEqual(addr.country, "FRANCE")
        self.assertEqual(addr.city, "Paris")
        self.assertEqual(addr.street_address, "Rue De Main")
        self.assertEqual(addr.zip_code, "54321")

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    @patch("questionary.text")
    def test_delete_address(self, mock_text, mock_select):
        mock_text.side_effect = [
            unittest.mock.Mock(ask=lambda: "Germany"),
            unittest.mock.Mock(ask=lambda: "Berlin"),
            unittest.mock.Mock(ask=lambda: "Main St"),
            unittest.mock.Mock(ask=lambda: "12345"),
        ]
        self.book.add_address()
        mock_select.return_value.ask.return_value = "0: Germany, Berlin, 12345, GERMANY"
        result = self.book.delete_address()
        self.assertIn("deleted", result)
        self.assertEqual(len(self.book._active_contact.addresses), 0)

    def test_show_addresses(self):
        with patch("questionary.text") as mock_text:
            mock_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "Germany"),
                unittest.mock.Mock(ask=lambda: "Berlin"),
                unittest.mock.Mock(ask=lambda: "Main St"),
                unittest.mock.Mock(ask=lambda: "12345"),
            ]
            self.book.add_address()
        result = self.book.show_addresses()
        self.assertIn("GERMANY", result)
        self.assertIn("Berlin", result)

    @patch("src.district_9_personal_assistant.selection.questionary.select")
    def test_set_main_address(self, mock_select):
        with patch("questionary.text") as mock_text:
            mock_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "Germany"),
                unittest.mock.Mock(ask=lambda: "Berlin"),
                unittest.mock.Mock(ask=lambda: "Main St"),
                unittest.mock.Mock(ask=lambda: "12345"),
            ]
            self.book.add_address()
            mock_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "France"),
                unittest.mock.Mock(ask=lambda: "Paris"),
                unittest.mock.Mock(ask=lambda: "Rue de Main"),
                unittest.mock.Mock(ask=lambda: "54321"),
            ]
            self.book.add_address()
        mock_select.return_value.ask.return_value = "1: France, Paris, 54321, FRANCE"
        result = self.book.set_main_address()
        addresses = self.book._active_contact.addresses
        self.assertIn("Main address set", result)
        self.assertTrue(addresses[1].is_main)
        self.assertFalse(addresses[0].is_main)


if __name__ == "__main__":
    unittest.main()
