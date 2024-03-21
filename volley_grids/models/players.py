"""Module with models of the players"""
from typing import Literal, TypeAlias
from uuid import uuid4

from pydantic import BaseModel, Field

GENDER: TypeAlias = Literal['M', 'W']


class Player(BaseModel):
    """Base model of the player

    Attributes:
        id:      unique identifier of the player, could be set any unique string, by default it's uuid4
        gender:     sex identifier of the player, could be 'M' or 'W'
        age:     age of the player
        name:    first name of the player
        surname: surname of the player
        points:  points of the player

    Returns:
        Player: instance of the player

    Raise:
        ValidationError: if any of the arguments is not valid

    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    gender: GENDER
    age: int | None = None
    name: str
    surname: str
    points: int = 0

    @property
    def full_name(self) -> str:
        """Return full name of the player

        Returns:
            str: full name of the player
        """
        return f'{self.name} {self.surname}'

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'{self.surname} {self.name[0]}.'


class WomenPlayer(Player):
    """Model of the player, which sex is 'W'"""

    gender: GENDER = 'W'


class MenPlayer(Player):
    """Model of the player, which sex is 'M'"""

    gender: GENDER = 'M'
