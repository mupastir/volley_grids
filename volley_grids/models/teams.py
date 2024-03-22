"""Module with models of the teams for the volleyball tournament"""
from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, Field, model_validator

from volley_grids.models.players import MenPlayer, Player, WomenPlayer

TEAM_GENDER: TypeAlias = Literal['Men`s', 'Women`s', 'Mixed']


class BaseTeam(BaseModel):
    """Base model of the team

    Attributes:
        player_one: first player of the team
        player_two: second player of the team
        gender: gender of the team, could be 'Men`s', 'Women`s' or 'Mixed'
    """

    player_one: Player
    player_two: Player
    gender: TEAM_GENDER

    @property
    def age(self) -> int:
        """Return average age of the team

        Returns:
            int: sum age of the team
        """
        return self.player_one.age + self.player_two.age

    @property
    def points(self) -> int:
        """Return sum of the points of the team

        Returns:
            int: sum of the points of the team
        """
        return self.player_one.points + self.player_two.points

    @property
    def players(self) -> set[Player]:
        """Return set of the players of the team

        Returns:
            set[Player]: list of the players of the team
        """
        return {self.player_one, self.player_two}

    def __hash__(self):
        return hash(self.player_one.id) + hash(self.player_two.id)

    def __repr__(self):
        return f'{self.player_one.__repr__()}/{self.player_two.__repr__()}'


class WomenTeam(BaseTeam):
    """Model of the team, which both players sex are 'W'"""

    player_one: WomenPlayer
    player_two: WomenPlayer
    gender: Literal['Women`s'] = 'Women`s'


class MenTeam(BaseTeam):
    """Model of the team, which both players sex are 'M'"""

    player_one: MenPlayer
    player_two: MenPlayer
    gender: Literal['Men`s'] = 'Men`s'


class MixedTeam(BaseTeam):
    """Model of the team, which one player is 'M' and the other is 'W'"""

    player_one: WomenPlayer | MenPlayer
    player_two: MenPlayer | WomenPlayer
    gender: Literal['Mixed'] = 'Mixed'

    @model_validator(mode='after')
    def validate_player_genders(self) -> 'MixedTeam':
        """Validate players of the team on gender. If both players are the same gender, raise ValueError

        Returns:
            MixedTeam: validated team

        Raises:
            ValueError: if both players
        """
        if type(self.player_one).__name__ is type(self.player_two).__name__:
            raise ValueError('Team should be consisted of the players of different genders')
        return self


class ByeTeam(BaseTeam):
    """Model of the bye team which is used in the tournament to fill the empty slots for minimal participants
    https://en.wikipedia.org/wiki/Bye_(sports)

    Attributes:
        player_one: None
        player_two: None
    """

    player_one: None = None
    player_two: None = None

    @property
    def age(self) -> int:
        """Return average age of the team

        Returns:
            int: sum age of the team, always 0
        """
        return 0

    @property
    def points(self) -> int:
        """Return sum of the points of the blank team

        Returns:
            int: sum of the points of the team, always 0
        """
        return 0


Team = Annotated[MenTeam | WomenTeam | MixedTeam, Field(discriminator='gender')]
