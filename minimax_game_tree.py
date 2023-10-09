import math
from utils import compute_state_score
from keys import MAX_PLAYER, MIN_PLAYER, STATE, ACTION, SCORE, CHILDREN


def create_game_tree(max_player, min_player, state, action=None):
    return {
        MAX_PLAYER: max_player,
        MIN_PLAYER: min_player,
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
            game_tree[MAX_PLAYER],
            game_tree[MIN_PLAYER],
            next_state,
            action)
        game_tree[CHILDREN][next_state.rep] = child
        expand(child)


def compute_score(game_tree):
    if game_tree[SCORE] is not None:
        return

    game_tree[MAX_PLAYER].extended_nodes += 1

    if game_tree[STATE].is_done():
        game_tree[SCORE] = compute_state_score(
            game_tree[STATE],
            game_tree[MAX_PLAYER],
            game_tree[STATE].scores)
        return game_tree[SCORE]

    if game_tree[STATE].next_player == game_tree[MAX_PLAYER]:
        game_tree[SCORE] = -math.inf
        for child in game_tree[CHILDREN].values():
            compute_score(child)
            game_tree[SCORE] = max(game_tree[SCORE], child[SCORE])
        return

    if game_tree[STATE].next_player == game_tree[MIN_PLAYER]:
        game_tree[SCORE] = math.inf
        for child in game_tree[CHILDREN].values():
            compute_score(child)
            game_tree[SCORE] = min(game_tree[SCORE], child[SCORE])
        return
