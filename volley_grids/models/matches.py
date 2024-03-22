"""Module with models of the matches"""
from datetime import datetime
from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, Field

from volley_grids.models.teams import BaseTeam

TOURNAMENT_STAGE: TypeAlias = Literal[
    'F',
    '3/4',
    'SF',
    '5-8',
    'QF',
    '9-12',
    'R12',
    'R16',
    '13-16',
    '17-32',
    'R24',
    'R32',
    '33-48',
    'R48',
    '49-64',
    'R64',
    'RR',
]
MATCH_TYPE: TypeAlias = Literal['full', 'short']


class BaseMatch(BaseModel):
    """Base model of the match

    Attributes:
        team_one:          first team of the match
        team_two:          second team of the match
        score_team_one:    score of the match
        score_team_two:    score of the match
        winner:            winner of the match
        looser:            looser of the match
        court_number:      number of the court where the match is played
        match_number:      number of the match
        stage:             stage of the tournament
        start_time:        start time of the match
        end_time:          end time of the match
        type:              type of the match
    """

    team_one: BaseTeam | None = None
    team_two: BaseTeam | None = None
    team_one_match_from: int | None = None
    team_two_match_from: int | None = None
    score_team_one: int
    score_team_two: int
    first_set_score_team_one: int | None = Field(gt=0, default=None)
    first_set_score_team_two: int | None = Field(gt=0, default=None)
    winner: BaseTeam | None = None
    looser: BaseTeam | None = None
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

    def __hash__(self):
        return hash(self.team_one) + hash(self.team_two)

    def __repr__(self):
        return f'{self.team_one.__repr__()} VS {self.team_two.__repr__()}'


class ShortMatch(BaseMatch):
    """Model of the short match, which plays only one set"""

    score_team_one: int = Field(le=1, gt=0, default=0)
    score_team_two: int = Field(le=1, gt=0, default=0)
    type: Literal['short'] = 'short'


class FullMatch(BaseMatch):
    """Model of the full match, which plays three sets"""

    score_team_one: int = Field(le=2, gt=0, default=0)
    score_team_two: int = Field(le=2, gt=0, default=0)
    second_set_score_team_one: int | None = Field(gt=0, default=None)
    second_set_score_team_two: int | None = Field(gt=0, default=None)
    third_set_score_team_one: int | None = Field(gt=0, default=None)
    third_set_score_team_two: int | None = Field(gt=0, default=None)
    type: Literal['full'] = 'full'


PRO_TOUR_MATCH_STAGE: TypeAlias = Literal[
    'F', 'SF', 'QF', 'R16', 'R18', 'Pool A', 'Pool B', 'Pool C', 'Pool D', 'Pool E', 'Pool F'
]


class ProTourMatch(FullMatch):
    """Model of the Pro Tour match, which has a different stage"""

    stage: PRO_TOUR_MATCH_STAGE


Match = Annotated[ShortMatch | FullMatch, Field(discriminator='type')]
