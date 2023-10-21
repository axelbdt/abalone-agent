from __future__ import annotations

import copy
import json
from typing import TYPE_CHECKING

from board_abalone import BoardAbalone
from seahorse.game.action import Action
from seahorse.game.game_layout.board import Piece
from seahorse.player.player import Player
from seahorse.utils.serializer import Serializable
from keys import COMPUTED_NODES, SUCCESSFUL_LOOKUPS, CUTOFFS

if TYPE_CHECKING:
    from game_state_abalone import GameStateAbalone


class PlayerAbalone(Player):
    """
    A player class for the Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", *args, **kwargs) -> None:
        """
        Initializes a new instance of the AlphaPlayerAbalone class.

        Args:
            piece_type (str): The type of the player's game piece.
            name (str, optional): The name of the player. Defaults to "bob".
        """
        super().__init__(name, *args, **kwargs)
        self.piece_type = piece_type
        self.info = {
            COMPUTED_NODES: 0,
            SUCCESSFUL_LOOKUPS: 0,
            CUTOFFS: 0
        }

    def increment_computed_nodes(self) -> None:
        """
        Increments the number of computed nodes by one.
        """
        self.info[COMPUTED_NODES] += 1

    def increment_successful_lookups(self) -> None:
        """
        Increments the number of successful lookups by one.
        """
        self.info[SUCCESSFUL_LOOKUPS] += 1

    def increment_cutoffs(self) -> None:
        """
        Increments the number of cutoffs by one.
        """
        self.info[CUTOFFS] += 1

    def get_piece_type(self) -> str:
        """
        Gets the type of the player's game piece.

        Returns:
            str: The type of the player's game piece.
        """
        return self.piece_type

    def to_json(self) -> str:
        return {i: j for i, j in self.__dict__.items() if i != "timer"}

    @classmethod
    def from_json(cls, data) -> Serializable:
        return PlayerAbalone(**json.loads(data))
