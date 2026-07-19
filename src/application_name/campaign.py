"""Defines the Campaign class."""
from datetime import date


class Campaign:
    """Represents a single ad campaign and the channels it runs on."""

    def __init__(self, name: str, company: str, budget: float = 0.0,
                 status: str = 'active', start_date: date = None,
                 end_date: date = None) -> None:
        """Initializes Campaign object with known state."""
        self.name = name
        self.company = company
        self.budget = budget
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self._channel_links = []  # each item: {'channel': Channel, 'spend': float, 'start_date': date}

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the object."""
        return f'{self.name} ({self.company}, ${self.budget}, {self.status})'

    def add_channel(self, channel, spend: float = 0.0, start_date: date = None) -> None:
        """Link a channel to this campaign, with the spend allocated to that pairing."""
        self._channel_links.append({
            'channel': channel,
            'spend': spend,
            'start_date': start_date
        })

    @property
    def total_spend(self) -> float:
        """Return the sum of spend across every linked channel."""
        return sum(link['spend'] for link in self._channel_links)

    @property
    def channel_count(self) -> int:
        """Return how many channels are linked to this campaign."""
        return len(self._channel_links)

    def list_channels(self) -> list:
        """Return the list of Channel objects linked to this campaign."""
        return [link['channel'] for link in self._channel_links]
