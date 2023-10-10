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
    """
    Expands the game tree by creating children nodes
    will expand the children nodes recursively until the game is done
    """
    if game_tree[CHILDREN] is not None:
        return game_tree

    game_tree[CHILDREN] = {
        action.get_next_game_state().rep:
        expand(create_game_tree(action.get_next_game_state(), action))
        for action in game_tree[STATE].get_possible_actions()
    }

    return game_tree


def compute_score(game_tree, max_player, min_player):
    """
    Computes the score of the game tree by expanding it completely
    and then computing the score of each node from the bottom up
    using the minimax algorithm
    """
    expand(game_tree)
    if game_tree[SCORE] is not None:
        return

    max_player.computed_nodes += 1

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
