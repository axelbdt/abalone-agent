from utils import score_and_distance, get_opponent
from keys import STATE
from my_player_ab import MyPlayer as MyPlayerAB


class MyPlayer(MyPlayerAB):
    """
    Player class for Abalone game.

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
        self.game_tree = None
        self.computed_nodes = 0
        self.heuristic = None
        self.table = {}

    def get_heuristic(self, state):
        opponent_id = get_opponent(state, self).get_id()
        self.heuristic = lambda x: score_and_distance(
            x[STATE], self.get_id(), opponent_id)
        return self.heuristic
