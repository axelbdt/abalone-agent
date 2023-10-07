import math
from utils import compute_score
from game_tree import GameTree


class MinimaxGameTree(GameTree):
    def get_value(self):
        if self.value is not None:
            return self.value

        self.max_player.extended_nodes += 1

        if self.state.is_done():
            self.value = compute_score(
                self.state, self.max_player, self.state.get_scores())
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
