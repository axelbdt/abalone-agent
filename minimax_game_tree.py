import math
from utils import compute_score
from game_tree_new import GameTree


class MinimaxGameTree(GameTree):
    def expand(self):
        if self.children is not None:
            return

        self.children = {}
        for action in self.state.get_possible_actions():
            next_state = action.get_next_game_state()
            child = MinimaxGameTree(
                self.max_player, self.min_player, next_state, action)
            self.children[next_state.rep] = child
            child.expand()

    def compute_score(self):
        if self.score is not None:
            return

        self.max_player.extended_nodes += 1

        if self.state.is_done():
            self.score = compute_score(
                self.state, self.max_player, self.state.scores)
            return self.score

        if self.state.next_player == self.max_player:
            self.score = -math.inf
            for child in self.get_children().values():
                child.compute_score()
                self.score = max(self.score, child.score)
            return

        if self.state.next_player == self.min_player:
            self.score = math.inf
            for child in self.get_children().values():
                child.compute_score()
                self.score = min(self.score, child.score)
            return
