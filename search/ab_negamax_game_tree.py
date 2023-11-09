from utils import compute_terminal_state_score, compute_normalized_distances_to_center
from keys import STATE, ACTION, SCORE, CHILDREN, ALPHA, BETA, TURN, NEXT, DEPTH
from math import inf


def create_game_tree(state, action=None):
    return {
        STATE: state,
        SCORE: None,
        NEXT: None,
        ACTION: action,
        CHILDREN: None,
        ALPHA: -inf,
        BETA: inf,
        DEPTH: -inf,
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
        create_game_tree(action.get_next_game_state(), action)
        for action in game_tree[STATE].get_possible_actions()
    }

    return game_tree


def compute_score(*, game_tree, depth=0, heuristic=None, table=None):
    """
    Computes the score of the game tree by expanding it completely
    and then computing the score of each node from the bottom up
    using the negamax algorithm
    """
    if game_tree[SCORE] is not None and game_tree[DEPTH] >= depth:
        return game_tree[SCORE]

    if table is not None:
        rep = game_tree[STATE].rep
        table_key = (rep, game_tree[STATE].step)
        lookup_result = table.get(table_key)
        if lookup_result is not None:
            game_tree[STATE].get_next_player().increment_successful_lookups()
            game_tree[SCORE] = lookup_result[SCORE]
            game_tree[NEXT] = lookup_result[NEXT]
            return game_tree[SCORE]

    game_tree[STATE].get_next_player().increment_computed_nodes()
    if depth == 0:
        # heuristic evaluates from next player (opponent) perspective
        game_tree[SCORE] = - heuristic(game_tree)
        game_tree[DEPTH] = 0
        return game_tree[SCORE]

    if game_tree[STATE].is_done():
        game_tree[SCORE] = compute_terminal_state_score(
            game_tree[STATE],
            game_tree[STATE].next_player)
        game_tree[DEPTH] = inf
        return game_tree[SCORE]

    expand(game_tree)
    game_tree[SCORE] = -inf
    children = game_tree[CHILDREN].values()
    if heuristic is not None:
        children = sorted(
            game_tree[CHILDREN].values(),
            key=heuristic,
            reverse=True)
    for child in children:
        child[ALPHA] = -game_tree[BETA]
        child[BETA] = -game_tree[ALPHA]
        compute_score(game_tree=child, depth=depth-1, heuristic=heuristic, table=table)
        game_tree[SCORE] = max(game_tree[SCORE], -child[SCORE])
        game_tree[ALPHA] = max(game_tree[ALPHA], game_tree[SCORE])
        if game_tree[ALPHA] >= game_tree[BETA]:
            game_tree[STATE].get_next_player().increment_cutoffs()
            break

    if table is not None:
        table[table_key] = {
            SCORE: game_tree[SCORE],
            NEXT: game_tree[NEXT],
        }

    game_tree[DEPTH] = depth
    return game_tree[SCORE]
