import random

import pytest

from tests.factories import MenPlayerFactory, WomenPlayerFactory
from volley_grids.seeders.king_of_the_beach import KingOfTheBeachSeeder


@pytest.mark.parametrize(
    'number_of_participants, number_of_teams, number_of_matches',
    [
        (4, 6, 3),
        (5, 10, 15),
        (6, 15, 45),
    ],
)
def test_success_king_of_the_beach_seed(number_of_participants: int, number_of_teams: int, number_of_matches: int):
    number_women_players = number_of_participants - random.randint(1, number_of_participants - 1)
    number_mens_players = number_of_participants - number_women_players
    participants = (  # type: ignore
        *WomenPlayerFactory.create_batch(size=number_women_players),
        *MenPlayerFactory.create_batch(size=number_mens_players),
    )
    seeder = KingOfTheBeachSeeder(participants=participants, match_type='short')
    matches = seeder.seed()
    assert len(seeder.teams) == number_of_teams
    assert len(matches) == number_of_matches
    assert len(set(matches)) == number_of_matches
