"""Module with models of the tournaments"""
from enum import StrEnum
from typing import Literal, TypeAlias

from pydantic import BaseModel

from volley_grids.models.matches import Match
from volley_grids.models.teams import TEAM_GENDER, BaseTeam


class TournamentType(StrEnum):
    """Enum of the tournament types"""

    DE = 'Double Elimination'
    SE = 'Single Elimination'
    RR = 'Round Robin'
    CH24 = 'Challenge 24'
    ELITE16 = 'Elite 16'
    KOB = 'King of the Beach'


TOURNAMENT_PLACES: TypeAlias = Literal['1', '2', '3', '4', '5-8', '9-12', '13-16', '17-24', '25-32', '33-48', '49-64']
Participants: TypeAlias = list[BaseTeam]


class TeamRestrictions(BaseModel):
    """Model of the team restrictions

    Attributes:
        max_age:     maximum age of the team
        team_gender: gender of the team, could be 'Men`s', 'Women`s' or 'Mixed'

    """

    max_age: int | None = None
    team_gender: TEAM_GENDER

    def validate_team(self, team: BaseTeam) -> bool:
        """Validate the team by the restrictions

        Args:
            team: team to validate

        Returns:
            bool: True if the team is valid, False otherwise
        """
        if self.max_age and team.age > self.max_age:
            return False
        if self.team_gender != team.gender:
            return False
        return True


class OnlyMensTeamsRestrictions(TeamRestrictions):
    """Restrictions for the men`s teams"""

    team_gender: Literal['Men`s']


class OnlyWomensTeamsRestrictions(TeamRestrictions):
    """Restrictions for the women`s teams"""

    team_gender: Literal['Women`s']


class MixedTeamsRestrictions(TeamRestrictions):
    """Restrictions for the mixed teams (one player is 'M' and the other is 'W')"""

    team_gender: Literal['Mixed']


class Tournament(BaseModel):
    """Model of the tournament"""

    name: str
    description: str | None = None
    start_date: str
    end_date: str
    type: TournamentType
    restrictions: TeamRestrictions
    participants: list[BaseTeam] | None = None
    matches: list[Match] | None = None
