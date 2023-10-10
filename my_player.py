from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from sorted_ab_game_tree import create_game_tree, compute_score, expand
from keys import SCORE, STATE, CHILDREN, ACTION
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
            players = current_state.get_players()
            self.opponent = (players[1] if players[0] == self
                             else players[0])
            self.game_tree = create_game_tree(current_state)
            compute_score(self.game_tree, self, self.opponent)

        # retrieve the current state in the tree after the opponent's move
        if current_state.rep != self.game_tree[STATE].rep:
            self.game_tree = self.game_tree[CHILDREN][current_state.rep]
            expand(self.game_tree)
            compute_score(self.game_tree, self, self.opponent)

        # compute the next state and action
        next_node = max(self.game_tree[CHILDREN].values(),
                        key=lambda x: x[SCORE] or -inf)
        chosen_action = next_node[ACTION]

        # use the next state as the root of the tree
        self.game_tree = next_node

        print("Node scores computed:", self.computed_nodes)
        return chosen_action

    def to_json(self) -> dict:
        return {}
