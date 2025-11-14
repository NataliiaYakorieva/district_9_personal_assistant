from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, fields, is_dataclass


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
        pass

    def to_dict(self) -> dict:
        """Converts the field to a dictionary for serialization."""
        return asdict(self)

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Abstract method to create a field instance from a dictionary."""
        raise NotImplementedError

    def update(self, new_data: dict) -> None:
        """
        Updates the fields of the instance with new data and re-validates.
        """
        if not is_dataclass(self):
            raise TypeError("update() is only supported for dataclass instances.")

        old_values = {}
        has_changes = False
        for field_info in fields(self):
            if field_info.name in new_data:
                old_value = getattr(self, field_info.name)
                new_value = new_data[field_info.name]
                old_values[field_info.name] = old_value
                if old_value != new_value:
                    has_changes = True
                setattr(self, field_info.name, new_value)
        
        if not has_changes:
            raise ValueError("No changes detected. The new value is the same as the current value.")

        # If validation fails, restore the old values
        try:
            self.validate()
        except (ValueError, TypeError) as e:
            for field_name, old_value in old_values.items():
                setattr(self, field_name, old_value)
            raise

    def __str__(self) -> str:
        """Default string representation."""
        return self.__class__.__name__
