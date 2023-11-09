from utils import compute_terminal_state_score, compute_normalized_distances_to_center
from keys import STATE, ACTION, SCORE, CHILDREN, ALPHA, BETA, TURN, NEXT, DEPTH
from math import inf


def create_game_tree(state, action=None):
    return {
        STATE: state,
        ACTION: action,
        CHILDREN: None,
        ALPHA: -inf,
        BETA: inf,
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


def compute_score(*, game_tree, depth=0, heuristic, table):
    """
    Computes the score of the game tree by expanding it completely
    and then computing the score of each node from the bottom up
    using the negamax algorithm
    """
    # turns_to_end = game_tree[STATE].step - game_tree[STATE].max_step 
    rep = game_tree[STATE].rep
    table_key = (rep, game_tree[STATE].step)
    lookup_result = table.get(table_key)
    if lookup_result is not None and lookup_result[DEPTH] >= depth:
        score = lookup_result[SCORE]
        game_tree[STATE].get_next_player().increment_successful_lookups()
        return score
    elif game_tree[STATE].is_done():
        score = compute_terminal_state_score(
            game_tree[STATE],
            game_tree[STATE].next_player)
        depth = inf
    elif depth == 0:
        # heuristic evaluates from next player (opponent) perspective
        score = - heuristic(game_tree)
    else:
        expand(game_tree)
        score = -inf
        children = sorted(
            game_tree[CHILDREN].values(),
            key=lambda x : compute_score(game_tree=x, depth=0, heuristic=heuristic, table=table))
            #reverse=True)
        for child in children:
            child[ALPHA] = -game_tree[BETA]
            child[BETA] = -game_tree[ALPHA]
            child_score = compute_score(game_tree=child, depth=depth-1, heuristic=heuristic, table=table)
            score = max(score, -child_score)
            game_tree[ALPHA] = max(game_tree[ALPHA], score)
            if game_tree[ALPHA] >= game_tree[BETA]:
                game_tree[STATE].get_next_player().increment_cutoffs()
                break

    table[table_key] = {
        SCORE: score,
        DEPTH: depth,
    }

    return score
