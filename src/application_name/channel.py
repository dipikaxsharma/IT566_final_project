"""Defines the Channel class."""


class Channel:
    """Represents a single distribution channel (e.g. Instagram Ads, Email)."""

    def __init__(self, name: str, type: str = 'other', status: str = 'active') -> None:
        """Initializes Channel object with known state."""
        self.name = name
        self.type = type
        self.status = status

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the object."""
        return f'{self.name} ({self.type}, {self.status})'
