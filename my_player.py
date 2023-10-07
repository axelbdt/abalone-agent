from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from sorted_ab_game_tree import SortedABGameTree


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
        self.extended_nodes = 0

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
            self.game_tree = SortedABGameTree(
                self, self.opponent, current_state)

        # retrieve the current state in the tree after the opponent's move
        if current_state.rep != self.game_tree.state.rep:
            self.game_tree = self.game_tree.get_children()[current_state.rep]

        # compute the next state and action
        next_state = max(self.game_tree.get_children().values(),
                         key=lambda x: x.get_value())
        chosen_action = next_state.action

        # use the next state as the root of the tree
        self.game_tree = next_state

        print(self.extended_nodes)
        return chosen_action
