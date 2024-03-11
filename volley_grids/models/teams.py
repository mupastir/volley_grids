from typing import Literal, TypeAlias

from pydantic import BaseModel

from volley_grids.models.players import MenPlayer, Player, WomenPlayer

TEAM_GENDER: TypeAlias = Literal['Men`s', 'Women`s', 'Mixed']


class Team(BaseModel):
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


class WomenTeam(Team):
    """Model of the team, which both players sex are 'W'"""

    player_one: WomenPlayer
    player_two: WomenPlayer
    gender: Literal['Women`s'] = 'Women`s'


class MenTeam(Team):
    """Model of the team, which both players sex are 'M'"""

    player_one: MenPlayer
    player_two: MenPlayer
    gender: Literal['Men`s'] = 'Men`s'


class MixedTeam(Team):
    """Model of the team, which one player is 'M' and the other is 'W'"""

    player_one: WomenPlayer
    player_two: MenPlayer
    gender: Literal['Mixed'] = 'Mixed'


class ByeTeam(Team):
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
