from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
import math
from typing import Dict


class GameTree:
    def __init__(self, max_player, min_player, state, action=None):
        self.min_player = min_player
        self.max_player = max_player
        self.state = state
        self.action = action
        self.value = None
        self.children = None

    def get_value(self):
        if self.value is not None:
            return self.value

        if self.state.is_done():
            self.value = self.compute_score(self.state.get_scores())
            return self.value

        if self.state.next_player == self.max_player:
            self.value = -math.inf
            for child in self.get_children().values():
                self.value = max(self.value, child.get_value())
            return self.value

        if self.state.next_player == self.min_player:
            self.value = math.inf
            for child in self.get_children().values():
                self.value = min(self.value, child.get_value())
            return self.value

    def get_children(self):
        if self.children is not None:
            return self.children

        self.children = {}
        for action in self.state.get_possible_actions():
            self.children[action.get_next_game_state().rep] = GameTree(self.max_player, self.min_player,
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

    def compute_score(self, scores: Dict[int, float]) -> int:
        """
        Computes the winners of the game based on the scores.

        Args:
            scores (Dict[int, float]): Score for each player

        Returns:
            Iterable[Player]: List of the players who won the game
        """
        def manhattanDist(A, B):
            dist = abs(B[0] - A[0]) + abs(B[1] - A[1])
            return dist

        max_val = max(scores.values())
        players_id = list(filter(lambda key: scores[key] == max_val, scores))
        itera = list(filter(lambda x: x.get_id()
                     in players_id, self.state.get_players()))
        if len(itera) > 1:  # égalité
            final_rep = self.state.get_rep()
            env = final_rep.get_env()
            dim = final_rep.get_dimensions()
            dist = dict.fromkeys(players_id, 0)
            center = (dim[0]//2, dim[1]//2)
            for i, j in list(env.keys()):
                p = env.get((i, j), None)
                if p.get_owner_id():
                    dist[p.get_owner_id()] += manhattanDist(center, (i, j))
            min_dist = min(dist.values())
            players_id = list(filter(lambda key: dist[key] == min_dist, dist))
            itera = list(filter(lambda x: x.get_id()
                         in players_id, self.state.get_players()))

        if len(itera) > 1:
            return 0

        if len(itera) == 1:
            if itera[0] == self.max_player:
                return 1
            else:
                return -1


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
            players = current_state.get_players()
            self.opponent = (players[1] if players[0] == self
                             else players[0])
            self.game_tree = GameTree(
                self, self.opponent, current_state)
            print(self.game_tree)
            print(self.game_tree.get_value())
        # TODO store children in dict with rep keys
        # rep = current_state.get_rep() # can be used as in dict
        # print(current_state.is_done())
        if current_state.rep != self.game_tree.state.rep:
            self.game_tree = self.game_tree.get_children()[current_state.rep]
        next_state = max(self.game_tree.get_children().values(),
                         key=lambda x: x.get_value())
        print(f"value next state: {next_state.get_value()}")
        chosen_action = next_state.action
        self.game_tree = next_state
        # print(choice.get_next_game_state().is_done())
        return chosen_action
