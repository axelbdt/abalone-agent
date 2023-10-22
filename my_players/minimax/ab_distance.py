from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from ab_game_tree import create_game_tree, compute_score, expand
from utils import distance_to_center, get_opponent
from keys import SCORE, STATE, CHILDREN, ACTION
from math import inf
from ab import MyPlayer as MyPlayerAB


class MyPlayer(MyPlayerAB):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def to_json(self) -> dict:
        return {}

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float = 60*15, *args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name, time_limit, *args)
        self.game_tree = None
        self.computed_nodes = 0
        self.heuristic = lambda x: -distance_to_center(x[STATE], self.get_id())
