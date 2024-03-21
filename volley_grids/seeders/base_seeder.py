"""Module with models of the matches"""
from abc import ABC, abstractmethod
from typing import Literal

from pydantic import TypeAdapter

from volley_grids.models.matches import Match
from volley_grids.models.tournaments import Participants, Tournament


class BaseSeeder(ABC):
    """Base class for seeding the matches of a tournament"""

    match_type_adapter = TypeAdapter(Match)

    def __init__(
        self, tournament: Tournament, participants: Participants, match_type: Literal['full', 'short']
    ) -> None:
        """Initialize the seeder

        Args:
            tournament: Tournament to seed
            participants: Participants of the tournament
            match_type: Type of the match, full or short
        """
        self.tournament = tournament
        self.participants = participants
        self.match_type = match_type

    @abstractmethod
    def seed(self) -> list[Match]:
        """Abstract method to seed the matches of the tournament"""
