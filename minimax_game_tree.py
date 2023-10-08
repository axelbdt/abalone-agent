import math
from utils import compute_score
from game_tree import GameTree


class MinimaxGameTree(GameTree):
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
                self.score = max(self.score, child.get_score())
            return self.score

        if self.state.next_player == self.min_player:
            self.score = math.inf
            for child in self.get_children().values():
                self.score = min(self.score, child.get_score())
            return self.score
