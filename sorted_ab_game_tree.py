from game_tree import GameTree
import math
from utils import compute_score, distance_to_center


class SortedABGameTree(GameTree):
    """
    game tree using alpha beta pruning
    with sorted children based on distance to center
    """

    def __init__(self, max_player, min_player, state, action=None):
        super().__init__(max_player, min_player, state, action)
        self.alpha = -math.inf
        self.beta = math.inf

    def get_score(self):
        if self.score is not None:
            return self.score

        self.max_player.extended_nodes += 1

        # terminal node
        if self.state.is_done():
            self.score = compute_score(
                self.state, self.max_player, self.state.get_scores())
            return self.score

        # MAX player
        if self.state.next_player == self.max_player:
            self.score = -math.inf

            # order children by distance to center
            children_list = self.get_children().values()
            ordered_children = sorted(
                children_list,
                key=lambda x: distance_to_center(x.state,
                                                 [self.max_player.get_id(),
                                                  self.min_player.get_id()],
                                                 self.max_player.get_id()))

            for child in ordered_children:
                child.alpha = self.alpha
                child.beta = self.beta
                self.score = max(self.score, child.get_score())
                self.alpha = max(self.alpha, self.score)
                if self.alpha >= self.beta:
                    break
            return self.score

        # MIN player
        if self.state.next_player == self.min_player:
            self.score = math.inf

            # order children by distance to center
            children_list = self.get_children().values()
            ordered_children = sorted(
                children_list,
                key=lambda x: distance_to_center(x.state,
                                                 [self.max_player.get_id(),
                                                  self.min_player.get_id()],
                                                 self.min_player.get_id()))

            for child in ordered_children:
                child.alpha = self.alpha
                child.beta = self.beta
                self.score = min(self.score, child.get_score())
                self.beta = min(self.beta, self.score)
                if self.alpha >= self.beta:
                    break
            return self.score
