
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

    def get_score(self):
        if self.score is not None:
            return self.score

        self.max_player.extended_nodes += 1

        if self.state.is_done():
            self.score = compute_score(
                self.state, self.max_player, self.state.get_scores())
            return self.score

        if self.state.next_player == self.max_player:
            self.score = -math.inf
            for child in self.get_children().values():
                child.alpha = self.alpha
                child.beta = self.beta
                self.score = max(self.score, child.get_score())
                self.alpha = max(self.alpha, self.score)
                if self.alpha >= self.beta:
                    break
            return self.score

        if self.state.next_player == self.min_player:
            self.score = math.inf
            for child in self.get_children().values():
                child.alpha = self.alpha
                child.beta = self.beta
                self.score = min(self.score, child.get_score())
                self.beta = min(self.beta, self.score)
                if self.alpha >= self.beta:
                    break
            return self.score
