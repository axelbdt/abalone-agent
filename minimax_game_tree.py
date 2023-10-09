import math
from utils import compute_state_score
from keys import STATE, ACTION, SCORE, CHILDREN


def create_game_tree(state, action=None):
    return {
        STATE: state,
        ACTION: action,
        SCORE: None,
        CHILDREN: None
    }


def expand(game_tree):
    if game_tree[CHILDREN] is not None:
        return

    game_tree[CHILDREN] = {}
    for action in game_tree[STATE].get_possible_actions():
        next_state = action.get_next_game_state()
        child = create_game_tree(
            next_state,
            action)
        game_tree[CHILDREN][next_state.rep] = child
        expand(child)


def compute_score(game_tree, max_player, min_player):
    if game_tree[SCORE] is not None:
        return

    if game_tree[STATE].is_done():
        game_tree[SCORE] = compute_state_score(
            game_tree[STATE],
            max_player,
            game_tree[STATE].scores)
        return game_tree[SCORE]

    if game_tree[STATE].next_player == max_player:
        game_tree[SCORE] = -math.inf
        for child in game_tree[CHILDREN].values():
            compute_score(child, max_player, min_player)
            game_tree[SCORE] = max(game_tree[SCORE], child[SCORE])
        return

    if game_tree[STATE].next_player == min_player:
        game_tree[SCORE] = math.inf
        for child in game_tree[CHILDREN].values():
            compute_score(child, max_player, min_player)
            game_tree[SCORE] = min(game_tree[SCORE], child[SCORE])
        return
