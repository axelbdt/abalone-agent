from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from search.negamax_game_tree import create_game_tree, expand, compute_score
from keys import STATE, ACTION, SCORE, CHILDREN
from math import inf


class MyPlayer(PlayerAbalone):
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
        if self.game_tree is None:
            self.game_tree = create_game_tree(current_state)
            expand(self.game_tree)
            compute_score(self.game_tree)

        if current_state.rep != self.game_tree[STATE].rep:
            self.game_tree = self.game_tree[CHILDREN][current_state.rep]

        next_state = max(self.game_tree[CHILDREN].values(),
                         key=lambda x: - (x[SCORE] or inf))
        chosen_action = next_state[ACTION]

        self.game_tree = next_state
        print(self.info)

        return chosen_action
