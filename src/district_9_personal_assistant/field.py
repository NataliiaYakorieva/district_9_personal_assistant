from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict


@dataclass
class BaseField(ABC):
    """
    Base class for all contact fields to provide a common interface
    for validation, serialization, and representation.
    """

    def __post_init__(self):
        """
        Ensures that validation is called after the dataclass is initialized.
        Subclasses should implement their normalization and validation logic here.
        """
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        """
        Abstract method to validate the field's data.
        Should raise ValueError for invalid data.
        """
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Converts the field to a dictionary for serialization."""
        return asdict(self)

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Abstract method to create a field instance from a dictionary."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Default string representation."""
        return self.__class__.__name__
