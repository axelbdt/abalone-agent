from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from search.ab_negamax_game_tree import create_game_tree, compute_score, expand
from keys import STATE, ACTION, SCORE, CHILDREN, NEXT, DEPTH, TURN
from keys import CUTOFFS, COMPUTED_NODES, SUCCESSFUL_LOOKUPS
from math import inf
from utils import get_opponent, score_and_distance_sym


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
        self.heuristic = lambda x: score_and_distance_sym(x[STATE])
        self.table = {}
        self.search_depth = 3

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
        # compute the tree on first run
        if self.game_tree is None:
            self.opponent = get_opponent(current_state, self)
            self.game_tree = create_game_tree(
                current_state)
            compute_score(
                game_tree=self.game_tree,
                depth = self.search_depth,
                heuristic=self.heuristic,
                table=self.table)

        # retrieve the current state in the tree after the opponent's move
        if current_state.rep != self.game_tree[STATE].rep:
            expand(self.game_tree)
            self.game_tree = self.game_tree[CHILDREN][current_state.rep]
            # will compute again if the opponent's move wasn't expanded

        expand(self.game_tree)
        # next_node = self.game_tree[NEXT]
        next_node = min(
                self.game_tree[CHILDREN].values(),
                key=lambda x: compute_score(game_tree=x, depth = self.search_depth - 1, heuristic=self.heuristic, table=self.table) or inf)

        chosen_action = next_node[ACTION]

        # use the next state as the root of the tree
        self.game_tree = next_node
        return chosen_action
