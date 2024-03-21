"""This module contains helper functions for the volley_grids app"""

from typing import Literal

from volley_grids.models.players import MenPlayer, Player, WomenPlayer


def get_team_gender(player_one: Player, player_two: Player) -> Literal['Men`s', 'Women`s', 'Mixed']:
    """Get team gender based on player types

    Args:
        player_one: first player
        player_two: second player

    Returns:
        str - one of the following: Men`s, Women`s, Mixed
    """
    if all(isinstance(player, WomenPlayer) for player in [player_one, player_two]):
        return 'Women`s'
    if all(isinstance(player, MenPlayer) for player in [player_one, player_two]):
        return 'Men`s'
    return 'Mixed'
