
import math
from utils import compute_score
from game_tree import GameTree


class ABGameTree(GameTree):
    """
    Game tree class for minimax with alpha-beta pruning.
    """

    def __init__(self, max_player, min_player, state, action=None):
        super().__init__(max_player, min_player, state, action)
        self.alpha = -math.inf
        self.beta = math.inf

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
                child.alpha = self.alpha
                child.beta = self.beta
                self.value = max(self.value, child.get_value())
                self.alpha = max(self.alpha, self.value)
                if self.alpha >= self.beta:
                    break
            return self.value

        if self.state.next_player == self.min_player:
            self.value = math.inf
            for child in self.get_children().values():
                self.value = min(self.value, child.get_value())
                self.beta = min(self.beta, self.value)
                if self.alpha >= self.beta:
                    break
            return self.value
