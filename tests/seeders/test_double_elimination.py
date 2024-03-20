from datetime import datetime, timedelta

import pytest

from tests.factories import MenTeamFactory, MixedTeamFactory, WomenTeamFactory
from volley_grids.models.matches import FullMatch
from volley_grids.models.teams import ByeTeam
from volley_grids.models.tournaments import Tournament, TournamentType
from volley_grids.seeders.double_elimination import DoubleEliminationSeeder


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
        type=TournamentType.DE.value,
        restrictions={'team_gender': gender},
        start_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        end_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
    )
    seeder = DoubleEliminationSeeder(participants=participants, tournament=tournament, match_type='full')
    matches = seeder.seed()
    sorted_participants = sorted(participants, key=lambda x: x.points, reverse=True)
    assert len(matches) == 14
    assert all(isinstance(match, FullMatch) for match in matches)
    assert matches[0].team_one == sorted_participants[0]
    assert isinstance(matches[0].team_two, ByeTeam)
    assert matches[1].team_one == sorted_participants[1]
    assert isinstance(matches[1].team_two, ByeTeam)
    assert matches[2].team_one == sorted_participants[2]
    assert isinstance(matches[2].team_two, ByeTeam)
    assert matches[3].team_one == sorted_participants[3]
    assert matches[3].team_two == sorted_participants[4]
    for i in range(5, 8):
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
def test_success_double_elimination_for_grid_of_sixteen(gender: str, team_factory):
    participants = MenTeamFactory.create_batch(size=10)
    tournament = Tournament(
        name='test tournament',
        type=TournamentType.DE.value,
        restrictions={'team_gender': gender},
        start_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        end_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
    )
    seeder = DoubleEliminationSeeder(participants=participants, tournament=tournament, match_type='full')
    matches = seeder.seed()
    sorted_participants = sorted(participants, key=lambda x: x.points, reverse=True)
    assert len(matches) == 30
    assert all(isinstance(match, FullMatch) for match in matches)
    assert matches[0].team_one == sorted_participants[0]
    assert isinstance(matches[0].team_two, ByeTeam)
    assert matches[1].team_one == sorted_participants[1]
    assert isinstance(matches[1].team_two, ByeTeam)
    assert matches[2].team_one == sorted_participants[2]
    assert isinstance(matches[2].team_two, ByeTeam)
    assert matches[3].team_one == sorted_participants[3]
    assert isinstance(matches[3].team_two, ByeTeam)
    assert matches[4].team_one == sorted_participants[4]
    assert isinstance(matches[4].team_two, ByeTeam)
    assert matches[5].team_one == sorted_participants[5]
    assert isinstance(matches[5].team_two, ByeTeam)
    assert matches[6].team_one == sorted_participants[6]
    assert matches[6].team_two == sorted_participants[9]
    assert matches[7].team_one == sorted_participants[7]
    assert matches[7].team_two == sorted_participants[8]
    for i in range(8, 16):
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
def test_success_double_elimination_for_grid_of_thirty_two(gender: str, team_factory):
    participants = MenTeamFactory.create_batch(size=30)
    tournament = Tournament(
        name='test tournament',
        type=TournamentType.DE.value,
        restrictions={'team_gender': gender},
        start_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        end_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
    )
    seeder = DoubleEliminationSeeder(participants=participants, tournament=tournament, match_type='full')
    matches = seeder.seed()
    sorted_participants = sorted(participants, key=lambda x: x.points, reverse=True)
    assert len(matches) == 62
    assert all(isinstance(match, FullMatch) for match in matches)
    assert matches[0].team_one == sorted_participants[0]
    assert isinstance(matches[0].team_two, ByeTeam)
    assert matches[1].team_one == sorted_participants[1]
    assert isinstance(matches[1].team_two, ByeTeam)
    assert matches[2].team_one == sorted_participants[2]
    assert matches[2].team_two == sorted_participants[29]
    assert matches[3].team_one == sorted_participants[3]
    assert matches[3].team_two == sorted_participants[28]
    assert matches[4].team_one == sorted_participants[4]
    assert matches[4].team_two == sorted_participants[27]
    assert matches[5].team_one == sorted_participants[5]
    assert matches[5].team_two == sorted_participants[26]
    assert matches[6].team_one == sorted_participants[6]
    assert matches[6].team_two == sorted_participants[25]
    assert matches[7].team_one == sorted_participants[7]
    assert matches[7].team_two == sorted_participants[24]
    assert matches[8].team_one == sorted_participants[8]
    assert matches[8].team_two == sorted_participants[23]
    assert matches[9].team_one == sorted_participants[9]
    assert matches[9].team_two == sorted_participants[22]
    assert matches[10].team_one == sorted_participants[10]
    assert matches[10].team_two == sorted_participants[21]
    assert matches[11].team_one == sorted_participants[11]
    assert matches[11].team_two == sorted_participants[20]
    assert matches[12].team_one == sorted_participants[12]
    assert matches[12].team_two == sorted_participants[19]
    assert matches[13].team_one == sorted_participants[13]
    assert matches[13].team_two == sorted_participants[18]
    assert matches[14].team_one == sorted_participants[14]
    assert matches[14].team_two == sorted_participants[17]
    assert matches[15].team_one == sorted_participants[15]
    assert matches[15].team_two == sorted_participants[16]
    for i in range(16, 32):
        assert matches[i].team_one is None
        assert matches[i].team_two is None
