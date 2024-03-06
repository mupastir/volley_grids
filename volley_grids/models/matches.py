from datetime import datetime
from typing import Literal, TypeAlias

from pydantic import BaseModel, Field

from volley_grids.models.teams import Team

TOURNAMENT_STAGE: TypeAlias = Literal[
    'F', '3/4', 'SF', '5-8', 'QF', '9-12', 'R16', '13-16', 'R32', '33-48', 'R64', '49-64'
]


class Match(BaseModel):
    """Base model of the match

    Attributes:
        team_one:          first team of the match
        team_two:          second team of the match
        score_team_one:    score of the match
        score_team_two:    score of the match
    """

    team_one: Team
    team_two: Team
    score_team_one: int = Field(le=2, gt=0, default=0)
    score_team_two: int = Field(le=2, gt=0, default=0)
    winner: Team | None
    court_number: int
    match_number: int
    stage: TOURNAMENT_STAGE
    start_time: datetime
    end_time: datetime | None
    type: Literal['full', 'short'] = 'full'

    @property
    def duration(self) -> int | None:
        """Return duration of the match in minutes

        Returns:
            int: duration of the match, in minutes, or None if the match is not finished
        """
        if not self.end_time:
            return None
        return (self.end_time - self.start_time).seconds // 60


class ShortMatch(Match):
    """Model of the short match, which plays only one set"""

    score_team_one: int = Field(le=1, gt=0, default=0)
    score_team_two: int = Field(le=1, gt=0, default=0)
    type = 'short'
