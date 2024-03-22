"""Module with models of the matches"""
from collections.abc import Generator
from itertools import chain

from volley_grids.models.matches import Match
from volley_grids.models.teams import BaseTeam, ByeTeam
from volley_grids.seeders.base_seeder import BaseSeeder


class DoubleEliminationSeeder(BaseSeeder):
    """Class for seeding the matches of the double elimination tournament
    more info: https://en.wikipedia.org/wiki/Double-elimination_tournament
    """

    winner_stages_map = {32: ('R64',), 16: ('R48',), 8: ('R16',), 4: ('R12',), 2: ('QF', 'SF')}
    looser_stages_map = {16: ('49-64', '33-48'), 8: ('17-32', '13-16'), 4: ('9-12', '9-12'), 2: ('5-8', '5-8')}
    grid_configurations = {8, 16, 32}

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
        number_of_games = grid_dimension * 2 - 2

        matches = list(
            chain(
                self.first_winner_round_matches_generator(best_ranked_teams, least_ranked_teams, grid_dimension),
                self.other_rounds_matches_generator(grid_dimension),
                (
                    self.match_type_adapter.validate_python(
                        {
                            'type': self.match_type,
                            'match_number': number_of_games - 1,
                            'stage': '3/4',
                            'team_one_match_from': number_of_games - 2,
                            'team_two_match_from': number_of_games - 3,
                        }
                    ),
                    self.match_type_adapter.validate_python(
                        {
                            'type': self.match_type,
                            'match_number': number_of_games,
                            'stage': 'F',
                            'team_one_match_from': number_of_games - 2,
                            'team_two_match_from': number_of_games - 3,
                        }
                    ),
                ),
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
        for grid_dimension in self.grid_configurations:
            min_grid = grid_dimension - participants_number
            if min_grid >= 0:
                return grid_dimension
        raise ValueError(f'Participants number {participants_number} is too small for the tournament')

    def _create_blank_teams(self, number: int) -> list[ByeTeam]:
        """Create the blank teams

        Args:
            number: number of the blank teams

        Returns:
            list[ByeTeam]: list of the blank teams
        """
        return [ByeTeam(gender=self.tournament.restrictions.team_gender) for _ in range(number)]

    def first_winner_round_matches_generator(
        self, best_ranked_teams: list[BaseTeam], least_ranked_teams: list[BaseTeam], grid_dimension: int
    ) -> Generator[Match, None, None]:
        """Generate the first round matches

        Args:
            best_ranked_teams: list of the best ranked teams
            least_ranked_teams: list of the least ranked teams
            grid_dimension: dimension of the grid

        Yields:
            Match: match of the tournament

        """
        matches_number = grid_dimension // 2
        for match_number, (team_best_rank, team_lowest_rank) in enumerate(zip(best_ranked_teams, least_ranked_teams)):
            yield self.match_type_adapter.validate_python(
                {
                    'team_one': team_best_rank,
                    'team_two': team_lowest_rank,
                    'type': self.match_type,
                    'match_number': match_number + 1,
                    'stage': self.winner_stages_map[matches_number][0],
                }
            )

    def other_rounds_matches_generator(self, grid_dimension: int) -> Generator[Match, None, None]:
        """Generate the other rounds matches

        Args:
            grid_dimension: dimension of the grid

        Yields:
            Match: match of the tournament

        """
        current_stage_matches_number = grid_dimension // 4
        start_match_number = grid_dimension // 2 + 1
        while current_stage_matches_number >= 2:
            end_match_number = start_match_number + current_stage_matches_number
            # we update end match number on start each iteration
            # cause in the end current_stage_matches_number cuts in half

            for stage in (
                *self.winner_stages_map[current_stage_matches_number],
                *self.looser_stages_map[current_stage_matches_number],
            ):
                # this loop iterating over tournament stages for each branch (winners and losers)
                for match_number in range(start_match_number, end_match_number):
                    # this loop iterating over matches in the current stage
                    yield self.match_type_adapter.validate_python(
                        {
                            'type': self.match_type,
                            'match_number': match_number,
                            'stage': stage,
                        }
                    )
                start_match_number = end_match_number
                end_match_number += current_stage_matches_number
            current_stage_matches_number //= 2
