from datetime import datetime
from typing import Annotated, Literal, TypeAlias, Union

from pydantic import BaseModel, Field

from volley_grids.models.teams import Team

TOURNAMENT_STAGE: TypeAlias = Literal[
    'F',
    '3/4',
    'SF',
    '5-8',
    'QF',
    '9-12',
    '9-16',
    'R16',
    '13-16',
    '17-24',
    '25-32',
    '13-32',
    'R32',
    '33-48',
    '33-64',
    'R48',
    '49-64',
    'R64',
]
MATCH_TYPE: TypeAlias = Literal['full', 'short']


class BaseMatch(BaseModel):
    """Base model of the match

    Attributes:
        team_one:          first team of the match
        team_two:          second team of the match
        score_team_one:    score of the match
        score_team_two:    score of the match
    """

    team_one: Team | None = None
    team_two: Team | None = None
    score_team_one: int
    score_team_two: int
    winner: Team | None = None
    court_number: int | None = None
    match_number: int
    stage: TOURNAMENT_STAGE
    start_time: datetime | None = None
    end_time: datetime | None = None
    type: MATCH_TYPE

    @property
    def duration(self) -> int | None:
        """Return duration of the match in minutes

        Returns:
            int: duration of the match, in minutes, or None if the match is not finished
        """
        if not self.end_time:
            return None
        return (self.end_time - self.start_time).seconds // 60


class ShortMatch(BaseMatch):
    """Model of the short match, which plays only one set"""

    score_team_one: int = Field(le=1, gt=0, default=0)
    score_team_two: int = Field(le=1, gt=0, default=0)
    type: Literal['short'] = 'short'


class FullMatch(BaseMatch):
    """Model of the full match, which plays three sets"""

    score_team_one: int = Field(le=2, gt=0, default=0)
    score_team_two: int = Field(le=2, gt=0, default=0)
    type: Literal['full'] = 'full'


Match = Annotated[Union[ShortMatch, FullMatch], Field(discriminator='type')]
