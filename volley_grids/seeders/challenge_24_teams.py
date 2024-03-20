from itertools import chain
from typing import Iterable

from volley_grids.models.matches import ProTourMatch
from volley_grids.models.teams import Team
from volley_grids.seeders.base_seeder import BaseSeeder


class Challenge24Seeder(BaseSeeder):
    """Class for seeding the matches of the challenge 24 teams tournament"""

    def seed(self) -> list[ProTourMatch]:
        """Seed the matches of the tournament

        Returns:
            list[Match]: list of the matches of the tournament
        """
        sorted_by_rank = sorted(self.participants, key=lambda x: x.points, reverse=True)
        pools = {
            f'Pool {pool}': (sorted_by_rank[i], sorted_by_rank[11 - i], sorted_by_rank[12 + i], sorted_by_rank[23 - i])
            for i, pool in enumerate('ABCDEF')
        }

    def seed_pool_games(self, pools: dict[str, list[Team]]) -> Iterable[ProTourMatch]:
        """Seed the matches of the pool games"""
        first_games_in_pool = (
            ProTourMatch(
                match_number=counter + 1,
                stage=name,
                team_one=pool[0],
                team_two=pool[-1],
            )
            for counter, (name, pool) in enumerate(pools.items())
        )
        second_games_in_pool = (
            ProTourMatch(
                type=self.match_type,
                match_number=counter + 7,
                stage=name,
                team_one=pool[1],
                team_two=pool[2],
            )
            for counter, (name, pool) in enumerate(pools.items())
        )
        third_games_in_pool = (
            ProTourMatch(
                type=self.match_type,
                match_number=counter + 13,
                stage=name,
                team_one_match_from=counter + 1,
                team_two_match_from=counter + 7,
            )
            for counter, (name, pool) in enumerate(pools.items())
        )
        fourth_games_in_pool = (
            ProTourMatch(
                type=self.match_type,
                match_number=counter + 19,
                stage=name,
                team_one_match_from=counter + 1,
                team_two_match_from=counter + 7,
            )
            for counter, (name, pool) in enumerate(pools.items())
        )
        return chain(
            first_games_in_pool,
            second_games_in_pool,
            third_games_in_pool,
            fourth_games_in_pool,
        )
