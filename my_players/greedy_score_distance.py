from greedy import MyPlayer as MyPlayerGreedy
from keys import STATE
from utils import heuristic_combined


class MyPlayer(MyPlayerGreedy):
    """
    Player class for Abalone game.
    The player will use the heuristic to compute the next best action (greedy approach).
    A different heuristic can be provided in subclasses.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float = 60*15, *args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name, time_limit, *args)
        self.heuristics_used = {
            "score": 1,
            "center": 1
            }
        self.heuristic = lambda x: heuristic_combined(x[STATE], self.heuristics_used)
