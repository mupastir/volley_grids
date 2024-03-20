from datetime import datetime, timedelta

import pytest

from tests.factories import MenTeamFactory, MixedTeamFactory, WomenTeamFactory
from volley_grids.models.tournaments import Tournament, TournamentType
from volley_grids.seeders.round_robin import RoundRobinSeeder


@pytest.mark.parametrize(
    'gender, team_factory',
    [
        ('Men`s', MenTeamFactory),
        ('Women`s', WomenTeamFactory),
        ('Mixed', MixedTeamFactory),
    ],
)
def test_success_double_elimination_for_grid_of_eight(gender: str, team_factory):
    participants = team_factory.create_batch(size=5)
    tournament = Tournament(
        name='test tournament',
        type=TournamentType.RR.value,
        restrictions={'team_gender': gender},
        start_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        end_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
    )
    seeder = RoundRobinSeeder(participants=participants, tournament=tournament, match_type='full')
    matches = seeder.seed()
    assert len(matches) == 10
