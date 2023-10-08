# Base class for minimax game trees
class GameTree:

    def __init__(self, max_player, min_player, state, action=None):
        self.max_player = max_player
        self.min_player = min_player
        self.state = state
        self.action = action
        self.score = None
        self.children = None

    def expand(self):
        raise NotImplementedError

    def compute_score(self):
        raise NotImplementedError

    def get_children(self):
        return self.children

    def __str__(self):
        return self.get_str(0)

    def get_str(self, depth):
        label = "MAX" if self.state.next_player == self.max_player else "MIN"
        string = "-" * depth + f"{label} {self.score}\n"
        if self.children is not None:
            for child in self.children.values():
                string += child.get_str(depth + 1)
        return string

    def to_json(self):
        return ""
