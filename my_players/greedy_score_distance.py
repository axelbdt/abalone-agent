from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from keys import STATE, ACTION
from utils import score_and_distance, get_opponent


class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.
    The player will use the heuristic to compute the next best action (greedy approach).
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
        self.heuristic = None
        self.round = 0

    def get_heuristic(self, state):
        opponent_id = get_opponent(state, self).get_id()
        self.heuristic = lambda x: score_and_distance(
            x[STATE], self.get_id(), opponent_id)
        return self.heuristic

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        # compute the best possible action from the heuristic
        children = {
            action.get_next_game_state().rep:
                {STATE: action.get_next_game_state(),
                 ACTION: action}
            for action in current_state.get_possible_actions()
        }
        self.heuristic = self.get_heuristic(current_state)
        chosen_action = max(children.values(), key=self.heuristic)[ACTION]

        self.round += 1
        print("Round:", self.round)

        return chosen_action

    def to_json(self):
        return ""
