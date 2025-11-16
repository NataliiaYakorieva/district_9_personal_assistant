from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from src.district_9_personal_assistant.field import BaseField


@dataclass
class Note(BaseField):
    """
    Represents a note associated with a contact,
    including content, creation date, optional title, and tags.
    """
    content: str
    title: Optional[str] = ""
    tags_string: Optional[str] = ""
    tags_list: List[str] = field(default_factory=list, init=False, repr=False)
    creation_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """
        Initialize tags from tags_string and validate.
        """
        if self.tags_string:
            self.add_tags(self.tags_string)
        super().__post_init__()

    def validate(self) -> None:
        """
        Validate that the note content is not empty.
        Raises ValueError if invalid.
        """
        if not self.content or not self.content.strip():
            raise ValueError("Note content cannot be empty.")

    def add_tags(self, tags_string: str) -> None:
        """
        Adds one or multiple tags to the note. Accepts tags separated by comma.
        Tags are converted to lowercase and only new, unique tags are added.

        Args:
            tags_string: Comma-separated string of tags.
        """
        tags_to_add = [tag.strip().lower()
                       for tag in tags_string.split(",") if tag.strip()]
        for t in tags_to_add:
            if t not in self.tags_list:
                self.tags_list.append(t)

    def update_note(
        self,
        content: str = "",
        tags_string: Optional[str] = "",
        title: Optional[str] = ""
    ) -> None:
        """
        Update the note's content, title, and tags.

        Args:
            content: New content for the note.
            tags_string: New tags string.
            title: New title for the note.
        """
        self.content = content
        self.title = title
        self.tags_string = tags_string
        self.tags_list.clear()
        self.add_tags(tags_string)

    def get_tags_list(self) -> List[str]:
        """
        Get the list of tags for the note.

        Returns:
            List of tags.
        """
        return self.tags_list

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """
        Create a Note instance from a dictionary.

        Args:
            data: Dictionary containing note data.

        Returns:
            Note instance.
        """
        if 'creation_date' in data and isinstance(data['creation_date'], str):
            data['creation_date'] = datetime.fromisoformat(data['creation_date'])
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Converts the note to a dictionary, ensuring datetime is a string.

        Returns:
            Dictionary representation of the note.
        """
        data = super().to_dict()
        data['creation_date'] = self.creation_date.isoformat()
        return data

    def __str__(self) -> str:
        tags_str = ", ".join(
            self.tags_list) if self.tags_list else "No tags added."
        title_str = f"Title: {self.title}\n" if self.title else ""
        return (
            f"{title_str}Note: {self.content}\n"
            f"Tags: {tags_str}\n"
            f"Created at: {self.creation_date.strftime('%Y-%m-%d %H:%M:%S')}"
        )
