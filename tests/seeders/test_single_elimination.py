from datetime import datetime, timedelta

import pytest

from tests.factories import MenTeamFactory, MixedTeamFactory, WomenTeamFactory
from volley_grids.models.matches import FullMatch
from volley_grids.models.teams import BlankTeam
from volley_grids.models.tournaments import Tournament
from volley_grids.seeders.single_elimination import SingleEliminationSeeder


@pytest.mark.parametrize(
    'gender, team_factory',
    [
        ('Men`s', MenTeamFactory),
        ('Women`s', WomenTeamFactory),
        ('Mixed', MixedTeamFactory),
    ],
)
@pytest.mark.skip(reason='TMP')
def test_success_single_elimination_for_grid_of_eight(gender: str, team_factory):
    participants = team_factory.create_batch(size=5)
    tournament = Tournament(
        name='test tournament',
        type='Single Elimination',
        restrictions={'team_gender': gender},
        start_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        end_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
    )
    seeder = SingleEliminationSeeder(participants=participants, tournament=tournament, match_type='full')
    matches = seeder.seed()
    sorted_participants = sorted(participants, key=lambda x: x.points, reverse=True)
    assert len(matches) == 7
    assert all(isinstance(match, FullMatch) for match in matches)
    assert matches[0].team_one == sorted_participants[0]
    assert isinstance(matches[0].team_two, BlankTeam)
    assert matches[1].team_one == sorted_participants[1]
    assert isinstance(matches[1].team_two, BlankTeam)
    assert matches[2].team_one == sorted_participants[2]
    assert isinstance(matches[2].team_two, BlankTeam)
    assert matches[3].team_one == sorted_participants[3]
    assert matches[3].team_two == sorted_participants[4]
    for i in range(5, 7):
        assert matches[i].team_one is None
        assert matches[i].team_two is None


@pytest.mark.parametrize(
    'gender, team_factory',
    [
        ('Men`s', MenTeamFactory),
        ('Women`s', WomenTeamFactory),
        ('Mixed', MixedTeamFactory),
    ],
)
def test_success_single_elimination_for_grid_of_sixteen(gender: str, team_factory):
    participants = MenTeamFactory.create_batch(size=10)
    tournament = Tournament(
        name='test tournament',
        type='Single Elimination',
        restrictions={'team_gender': gender},
        start_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        end_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
    )
    seeder = SingleEliminationSeeder(participants=participants, tournament=tournament, match_type='full')
    matches = seeder.seed()
    sorted_participants = sorted(participants, key=lambda x: x.points, reverse=True)
    assert len(matches) == 15
    assert all(isinstance(match, FullMatch) for match in matches)
    assert matches[0].team_one == sorted_participants[0]
    assert isinstance(matches[0].team_two, BlankTeam)
    assert matches[1].team_one == sorted_participants[1]
    assert isinstance(matches[1].team_two, BlankTeam)
    assert matches[2].team_one == sorted_participants[2]
    assert isinstance(matches[2].team_two, BlankTeam)
    assert matches[3].team_one == sorted_participants[3]
    assert isinstance(matches[3].team_two, BlankTeam)
    assert matches[4].team_one == sorted_participants[4]
    assert isinstance(matches[4].team_two, BlankTeam)
    assert matches[5].team_one == sorted_participants[5]
    for i in range(5, 15):
        assert matches[i].team_one is None
        assert matches[i].team_two is None
