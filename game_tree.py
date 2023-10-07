# Base class for minimax game trees
class GameTree:

    def __init__(self, max_player, min_player, state, action=None):
        self.max_player = max_player
        self.min_player = min_player
        self.state = state
        self.action = action
        self.value = None
        self.children = None

    def get_children(self):
        if self.children is not None:
            return self.children

        self.children = {}
        for action in self.state.get_possible_actions():
            rep = action.get_next_game_state().rep
            self.children[rep] = self.__class__(self.max_player, self.min_player,
                                                action.get_next_game_state(), action)
        return self.children

    def get_value(self):
        raise NotImplementedError

    def __str__(self):
        return self.get_str(0)

    def get_str(self, depth):
        label = "MAX" if self.state.next_player == self.max_player else "MIN"
        string = "-" * depth + f"{label} {self.value}\n"
        if self.children is not None:
            for child in self.children.values():
                string += child.get_str(depth + 1)
        return string

    def to_json(self):
        return ""
