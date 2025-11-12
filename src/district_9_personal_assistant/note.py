from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Note:
    """
    Represents a note associated with a contact,
    including content, creation date, optional title, and tags.
    """
    content: str
    title: Optional[str] = ""
    tags_string: Optional[str] = ""
    tags_list: List[str] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        self.creation_date = datetime.now()
        if self.tags_string:
            self.add_tags(self.tags_string)

    def add_tags(self, tags_string: str):
        """
        Adds one or multiple tags to the note. Accepts tags separated by comma.
        Tags are converted to lowercase and only new, unique tags are added.
        Example: "meeting, follow-up, urgent"
        """
        tags_to_add = [tag.strip().lower()
                       for tag in tags_string.split(",") if tag.strip()]
        for t in tags_to_add:
            if t not in self.tags_list:
                self.tags_list.append(t)

    def edit_content(self, content: str):
        self.content = content

    def edit_title(self, title: str):
        self.title = title

    def get_tags_list(self) -> List[str]:
        return self.tags_list

    def __str__(self):
        tags_str = ", ".join(self.tags_list)
        title_str = f"Title: {self.title}\n" if self.title else ""
        return f"{title_str}Note: {
            self.content}\nTags: {tags_str}\nCreated at: {
            self.creation_date.strftime('%Y-%m-%d %H:%M:%S')}"
