"""Module with matches seeder for the round-robin tournament"""
from itertools import combinations

from volley_grids.models.matches import Match
from volley_grids.seeders.base_seeder import BaseSeeder


class RoundRobinSeeder(BaseSeeder):
    """Class for seeding the matches of the round-robin tournament
    more info: https://en.wikipedia.org/wiki/Round-robin_tournament
    """

    def seed(self) -> list[Match]:
        """Seed the matches of the tournament

        Returns:
            list[Match]: list of the matches of the tournament
        """
        matches = [
            self.match_type_adapter.validate_python(
                {
                    'type': self.match_type,
                    'match_number': counter + 1,
                    'team_one': team_one,
                    'team_two': team_two,
                    'stage': 'RR',
                }
            )
            for counter, (team_one, team_two) in enumerate(combinations(self.participants, 2))
        ]
        return matches
