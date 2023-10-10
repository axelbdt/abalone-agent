
import math
from utils import compute_state_score
from keys import STATE, ACTION, SCORE, CHILDREN, ALPHA, BETA


def create_game_tree(state, action=None):
    return {
        STATE: state,
        ACTION: action,
        SCORE: None,
        CHILDREN: None,
        ALPHA: -math.inf,
        BETA: math.inf
    }


def expand(game_tree):
    """
    Expands the game tree by creating children nodes,
    will only go one level deep
    """
    if game_tree[CHILDREN] is not None:
        return game_tree

    game_tree[CHILDREN] = {
        action.get_next_game_state().rep:
        create_game_tree(action.get_next_game_state(), action)
        for action in game_tree[STATE].get_possible_actions()
    }

    return game_tree


def compute_score(game_tree, max_player, min_player):
    """
    Computes the score of the game tree by expanding it completely
    and then computing the score of each node from the bottom up
    using the minimax algorithm with alpha-beta pruning
    pruned nodes will have their score set to None
    """
    expand(game_tree)
    if game_tree[SCORE] is not None:
        return game_tree[SCORE]

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
            # propagate alpha and beta values to child
            child[ALPHA] = game_tree[ALPHA]
            child[BETA] = game_tree[BETA]
            compute_score(child, max_player, min_player)
            game_tree[SCORE] = max(game_tree[SCORE], child[SCORE])
            game_tree[ALPHA] = max(game_tree[ALPHA], game_tree[SCORE])
            if game_tree[ALPHA] >= game_tree[BETA]:
                break
        return

    if game_tree[STATE].next_player == min_player:
        game_tree[SCORE] = math.inf
        for child in game_tree[CHILDREN].values():
            # propagate alpha and beta values to child
            child[ALPHA] = game_tree[ALPHA]
            child[BETA] = game_tree[BETA]
            compute_score(child, max_player, min_player)
            game_tree[SCORE] = min(game_tree[SCORE], child[SCORE])
            game_tree[BETA] = min(game_tree[BETA], game_tree[SCORE])
            if game_tree[ALPHA] >= game_tree[BETA]:
                break
        return
