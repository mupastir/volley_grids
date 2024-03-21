import pytest
from pydantic import TypeAdapter

from tests.factories import MenPlayerFactory, WomenPlayerFactory
from volley_grids.models.teams import MenTeam, MixedTeam, Team, WomenTeam

team_type_adapter = TypeAdapter(Team)


@pytest.mark.parametrize(
    'first_player_factory, second_player_factory, team_gender, expected_team_class',
    (
        (MenPlayerFactory, MenPlayerFactory, 'Men`s', MenTeam),
        (WomenPlayerFactory, WomenPlayerFactory, 'Women`s', WomenTeam),
        (MenPlayerFactory, WomenPlayerFactory, 'Mixed', MixedTeam),
        (WomenPlayerFactory, MenPlayerFactory, 'Mixed', MixedTeam),
    ),
)
def test_teams_models(first_player_factory, second_player_factory, team_gender, expected_team_class):
    player_one = first_player_factory.create()
    player_two = second_player_factory.create()

    mens_team = team_type_adapter.validate_python(
        {'player_one': player_one, 'player_two': player_two, 'gender': team_gender}
    )
    assert isinstance(mens_team, expected_team_class)
