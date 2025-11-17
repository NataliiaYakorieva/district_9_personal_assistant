import unittest
import re
from unittest.mock import patch

from src.district_9_personal_assistant.address_book import AddressBook


def strip_ansi(text):
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


questionary_select_path = "src.district_9_personal_assistant.selection.questionary.select"


class TestNoteBookFlows(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "John Doe"
            self.book.add_contact()

        with patch(questionary_select_path) as mock_select:
            mock_select.return_value.ask.return_value = "0: John Doe"
            self.book.select_active_contact()

    @patch("questionary.text")
    def test_add_note(self, mock_text):
        mock_text.side_effect = [
            unittest.mock.Mock(ask=lambda: "Meeting notes"),
            unittest.mock.Mock(ask=lambda: "Discussed project timeline."),
            unittest.mock.Mock(ask=lambda: "meeting, project")
        ]
        result = self.book.add_note()
        self.assertIn("Note added.", strip_ansi(result))
        notes = self.book.get_active_contact().notes
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].title, "Meeting notes")
        self.assertIn("meeting", notes[0].tags_list)
        self.assertIn("project", notes[0].tags_list)

    @patch(questionary_select_path)
    @patch("questionary.text")
    def test_edit_note(self, mock_text, mock_select):
        with patch("questionary.text") as add_text:
            add_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "Meeting notes"),
                unittest.mock.Mock(ask=lambda: "Discussed project timeline."),
                unittest.mock.Mock(ask=lambda: "meeting, project")
            ]
            self.book.add_note()

        mock_select.return_value.ask.return_value = "0: Meeting notes"
        mock_text.side_effect = [
            unittest.mock.Mock(ask=lambda: "Updated notes"),
            unittest.mock.Mock(ask=lambda: "Updated content."),
            unittest.mock.Mock(ask=lambda: "update, follow-up")
        ]
        result = self.book.edit_note()
        self.assertIn("updated", result)
        note = self.book.get_active_contact().notes[0]
        self.assertEqual(note.title, "Updated notes")
        self.assertEqual(note.content, "Updated content.")
        self.assertIn("update", note.tags_list)
        self.assertIn("follow-up", note.tags_list)

    @patch(questionary_select_path)
    def test_delete_note(self, mock_select):
        with patch("questionary.text") as add_text:
            add_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "Meeting notes"),
                unittest.mock.Mock(ask=lambda: "Discussed project timeline."),
                unittest.mock.Mock(ask=lambda: "meeting, project")
            ]
            self.book.add_note()

        mock_select.return_value.ask.return_value = "0: Meeting notes"
        result = self.book.delete_note()
        self.assertIn("deleted", result)
        self.assertEqual(len(self.book.get_active_contact().notes), 0)

    def test_show_notes(self):
        with patch("questionary.text") as mock_text:
            mock_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "Meeting notes"),
                unittest.mock.Mock(ask=lambda: "Discussed project timeline."),
                unittest.mock.Mock(ask=lambda: "meeting, project")
            ]
            self.book.add_note()
        result = self.book.show_notes()
        self.assertIn("Meeting notes", result)
        self.assertIn("Discussed project timeline.", result)

    @patch("questionary.text")
    def test_find_note(self, mock_text):
        with patch("questionary.text") as add_text:
            add_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "Meeting notes"),
                unittest.mock.Mock(ask=lambda: "Discussed project timeline."),
                unittest.mock.Mock(ask=lambda: "meeting, project")
            ]
            self.book.add_note()
        mock_text.return_value.ask.return_value = "project"
        result = self.book.find_note()
        result_str = str(result)
        self.assertIn("Meeting notes", result_str)
        self.assertIn("project", result_str)

    @patch("questionary.text")
    def test_find_by_tag(self, mock_text):
        with patch("questionary.text") as add_text:
            add_text.side_effect = [
                unittest.mock.Mock(ask=lambda: "Meeting notes"),
                unittest.mock.Mock(ask=lambda: "Discussed project timeline."),
                unittest.mock.Mock(ask=lambda: "meeting, project")
            ]
            self.book.add_note()
        mock_text.return_value.ask.return_value = "meeting"
        result = self.book.find_by_tag()
        self.assertIn("Meeting notes", str(result))
        self.assertIn("meeting", str(result))


if __name__ == "__main__":
    unittest.main()
