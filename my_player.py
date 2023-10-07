from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
import math
from utils import compute_score, compute_distance_to_center


class GameTree:
    def __init__(self, max_player, min_player, state, action=None):
        self.max_player = max_player
        self.min_player = min_player
        self.state = state
        self.action = action
        self.value = None
        self.children = None
        self.alpha = -math.inf
        self.beta = math.inf

    def get_value(self):
        if self.value is not None:
            return self.value

        self.max_player.extended_nodes += 1

        # terminal node
        if self.state.is_done():
            self.value = compute_score(
                self.state, self.max_player, self.state.get_scores())
            return self.value

        # MAX player
        if self.state.next_player == self.max_player:
            self.value = -math.inf

            # order children by distance to center
            children_list = self.get_children().values()
            ordered_children = sorted(
                children_list,
                key=lambda x: x.distance_to_center(self.max_player.get_id()))

            for child in ordered_children:
                child.alpha = self.alpha
                child.beta = self.beta
                self.value = max(self.value, child.get_value())
                self.alpha = max(self.alpha, self.value)
                if self.alpha >= self.beta:
                    break
            return self.value

        # MIN player
        if self.state.next_player == self.min_player:
            self.value = math.inf

            # order children by distance to center
            children_list = self.get_children().values()
            ordered_children = sorted(
                children_list,
                key=lambda x: x.distance_to_center(self.min_player.get_id()))

            for child in ordered_children:
                self.value = min(self.value, child.get_value())
                self.beta = min(self.beta, self.value)
                if self.alpha >= self.beta:
                    break
            return self.value

    def get_children(self):
        if self.children is not None:
            return self.children

        self.children = {}
        for action in self.state.get_possible_actions():
            rep = action.get_next_game_state().rep
            self.children[rep] = GameTree(self.max_player, self.min_player,
                                          action.get_next_game_state(), action)
        return self.children

    def __str__(self):
        return self.get_str(0)

    def get_str(self, depth):
        label = "MAX" if self.state.next_player == self.max_player else "MIN"
        string = "-" * depth + f"{label} {self.get_value()}\n"
        for child in self.get_children().values():
            string += child.get_str(depth + 1)
        return string

    def to_json(self):
        return {}

    def distance_to_center(self, player_id):
        dist = compute_distance_to_center(self.state,
                                          [self.max_player.get_id(),
                                           self.min_player.get_id()])
        return dist[player_id]


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
            self.game_tree = GameTree(
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
