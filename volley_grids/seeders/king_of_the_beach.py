"""Seeder for the king of the beach tournament"""
from itertools import combinations
from typing import Literal

from pydantic import TypeAdapter

from volley_grids.misc.helpers import get_team_gender
from volley_grids.models.matches import Match
from volley_grids.models.players import MenPlayer, WomenPlayer
from volley_grids.models.teams import Team

KingOfTheBeachParticipants = tuple[WomenPlayer | MenPlayer]


class KingOfTheBeachSeeder:
    """Class for seeding the matches of the king of the beach tournament.

    This is format of tournament where every player plays with every other player.

    """

    match_type_adapter = TypeAdapter(Match)
    team_type_adapter = TypeAdapter(Team)

    def __init__(self, participants: KingOfTheBeachParticipants, match_type: Literal['full', 'short']) -> None:
        """Initialize the seeder

        Args:
            participants: Participants of the tournament
            match_type: Type of the match, full or short
        """
        self.participants = participants
        self.match_type = match_type
        self.teams = []

    def seed(self) -> list[Match]:
        """Seed the matches of the tournament

        Returns:
            list[Match]: list of the matches of the tournament
        """
        self.teams = [
            self.team_type_adapter.validate_python(
                {'player_one': player_one, 'player_two': player_two, 'gender': get_team_gender(player_one, player_two)}
            )
            for player_one, player_two in combinations(self.participants, 2)
        ]
        matches = [
            self.match_type_adapter.validate_python(
                {
                    'type': self.match_type,
                    'match_number': match_number + 1,
                    'stage': 'RR',
                    'team_one': team_one,
                    'team_two': team_two,
                }
            )
            for match_number, (team_one, team_two) in enumerate(combinations(self.teams, 2))
            if not self.team_intersects(team_one, team_two)
        ]
        return matches

    @staticmethod
    def team_intersects(team_one: Team, team_two: Team) -> bool:
        """Check if the teams intersect

        Args:
            team_one: first team
            team_two: second team

        Returns:
            bool: True if the teams intersect, False otherwise
        """
        return bool(team_one.players & team_two.players)
