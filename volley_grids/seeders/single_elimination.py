from itertools import chain
from typing import Generator

from pydantic import TypeAdapter

from volley_grids.models.matches import Match
from volley_grids.models.teams import BlankTeam, Team
from volley_grids.seeders.base_seeder import BaseSeeder


class SingleEliminationSeeder(BaseSeeder):
    """Class for seeding the matches of the single elimination tournament
    more info: https://en.wikipedia.org/wiki/Single-elimination_tournament
    """

    grid_configurations = {
        8: (('5-8', 4), ('SF', 2), ('F', 1)),
        16: (('9-16', 8), ('5-8', 4), ('SF', 2), ('F', 1)),
        32: (('17-32', 16), ('9-16', 8), ('5-8', 4), ('SF', 2), ('F', 1)),
        64: (('33-64', 32), ('17-32', 16), ('9-16', 8), ('5-8', 4), ('SF', 2), ('F', 1)),
    }
    match_type_adapter = TypeAdapter(Match)

    def seed(self) -> list[Match]:
        """Seed the matches of the tournament

        Returns:
            list[Match]: list of the matches of the tournament
        """
        participants_number = len(self.participants)
        grid_dimension = self._choose_grid(participants_number)

        number_blank_teams = grid_dimension - participants_number
        self.participants.extend(self._create_blank_teams(number_blank_teams))
        sorted_participants = sorted(self.participants, key=lambda x: x.points, reverse=True)

        best_ranked_teams = sorted_participants[: grid_dimension // 2]
        least_ranked_teams = sorted_participants[grid_dimension // 2 :]
        least_ranked_teams.reverse()

        matches = list(
            chain(
                self.first_round_matches_generator(best_ranked_teams, least_ranked_teams, grid_dimension),
                self.other_round_matches_generator(participants_number, grid_dimension),
            )
        )
        return matches

    def _choose_grid(self, participants_number: int) -> int:
        """Choose the grid dimension for the tournament

        Args:
            participants_number: number of the participants

        Returns:
            int: dimension of the grid
        """
        for grid_dimension in self.grid_configurations.keys():
            min_grid = grid_dimension - participants_number
            if min_grid >= 0:
                return grid_dimension
        raise ValueError(f'Participants number {participants_number} is too small for the tournament')

    def _create_blank_teams(self, number: int) -> list[BlankTeam]:
        """Create the blank teams

        Args:
            number: number of the blank teams

        Returns:
            list[BlankTeam]: list of the blank teams
        """
        return [BlankTeam(gender=self.tournament.restrictions.team_gender) for _ in range(number)]

    def first_round_matches_generator(
        self, best_ranked_teams: list[Team], least_ranked_teams: list[Team], grid_dimension: int
    ) -> Generator[Match, None, None]:
        """Generate the first round matches

        Args:
            best_ranked_teams: list of the best ranked teams
            least_ranked_teams: list of the least ranked teams
            grid_dimension: dimension of the grid

        Yields:
            Match: match of the tournament

        """
        for match_number, (team_best_rank, team_lowest_rank) in enumerate(zip(best_ranked_teams, least_ranked_teams)):
            yield self.match_type_adapter.validate_python(
                {
                    'team_one': team_best_rank,
                    'team_two': team_lowest_rank,
                    'type': self.match_type,
                    'match_number': match_number + 1,
                    'stage': self.grid_configurations[grid_dimension][0][0],
                }
            )

    def other_round_matches_generator(
        self, participants_number: int, grid_dimension: int
    ) -> Generator[Match, None, None]:
        """Generate the other round matches

        Args:
            participants_number: number of the participants
            grid_dimension: dimension of the grid

        Yields:
            Match: match of the tournament

        """
        for match_number in range(participants_number + 1, participants_number * 2 - 1):
            yield self.match_type_adapter.validate_python(
                {
                    'type': self.match_type,
                    'match_number': match_number,
                    # Fixme: match_number >> 2 doesn't work as expected
                    'stage': self.grid_configurations[grid_dimension][(match_number >> 2) - 1][0],
                }
            )
