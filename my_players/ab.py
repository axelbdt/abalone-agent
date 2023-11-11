from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from search.ab_negamax_game_tree import compute_state_score
from keys import STATE, ACTION, SCORE, CHILDREN, NEXT, DEPTH, TURN
from keys import CUTOFFS, COMPUTED_NODES, SUCCESSFUL_LOOKUPS
from math import inf
from utils import get_opponent, score_and_distance_sym, get_pushes2


class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.
    The player will use the alpha-beta pruning algorithm to compute the best action.
    A different heuristic can be provided in subclasses

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
        self.heuristic = score_and_distance_sym
        self.table = {}
        self.search_depth = 3
        self.quiescence_test = lambda x: get_pushes2(x) == 0

    def to_json(self):
        return ""

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        # Play fast if quiescent state or no time left
        if self.quiescence_test(current_state) or self.get_remaining_time() < 10:
            depth = 2
            quiescence_test = None
        else:
            depth = self.search_depth
            quiescence_test = self.quiescence_test
        print(quiescence_test)
        print("Depth: ", depth)
        next_action = max(
                current_state.get_possible_actions(),
                key=lambda x: -compute_state_score(
                    x.get_next_game_state(),
                    depth = depth-1,
                    heuristic=self.heuristic,
                    table=self.table,
                    quiescence_test=None))

        return next_action
