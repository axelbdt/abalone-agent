
import math
from utils import compute_terminal_state_score
from keys import STATE, ACTION, DEPTH, SCORE, CHILDREN, ALPHA, BETA, NEXT


def create_game_tree(state,  action=None, depth=0):
    return {
        STATE: state,
        DEPTH: depth,
        ACTION: action,
        SCORE: None,
        CHILDREN: None,
        ALPHA: -math.inf,
        BETA: math.inf,
        NEXT: None
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
        create_game_tree(action.get_next_game_state(),
                         action, game_tree[DEPTH] + 1)
        for action in game_tree[STATE].get_possible_actions()
    }

    return game_tree


def compute_score(*,
                  game_tree,
                  max_player,
                  min_player,
                  heuristic=None,
                  table=None
                  ):
    """
    Computes the score of the game tree by expanding it completely
    and then computing the score of each node from the bottom up
    using the minimax algorithm with alpha-beta pruning
    pruned nodes will have their score set to None
    children are sorted according to a heuristic to improve pruning
    """
    expand(game_tree)
    if game_tree[SCORE] is not None:
        return game_tree[SCORE]

    # TODO: check that lookup state is not deeper than current state
    if table is not None:
        rep = game_tree[STATE].rep
        player_id = game_tree[STATE].next_player.get_id()
        table_key = (rep, player_id, game_tree[DEPTH])
        table_result = table.get(table_key)
        if table_result is not None:
            game_tree[STATE].get_next_player().increment_successful_lookups()
            game_tree[SCORE] = table_result[SCORE]
            game_tree[NEXT] = table_result[NEXT]
            return game_tree[SCORE]

    game_tree[STATE].get_next_player().increment_computed_nodes()

    if game_tree[STATE].is_done():
        game_tree[SCORE] = compute_terminal_state_score(
            game_tree[STATE],
            max_player)
        return game_tree[SCORE]

    if game_tree[STATE].next_player == max_player:
        game_tree[SCORE] = -math.inf
        children = game_tree[CHILDREN].values()
        if heuristic is not None:
            children = sorted(children, key=heuristic, reverse=True)
        for child in children:
            # propagate alpha and beta values to child
            child[ALPHA] = game_tree[ALPHA]
            child[BETA] = game_tree[BETA]
            compute_score(
                game_tree=child,
                max_player=max_player,
                min_player=min_player,
                heuristic=heuristic,
                table=table)
            game_tree[SCORE] = max(game_tree[SCORE], child[SCORE])
            game_tree[ALPHA] = max(game_tree[ALPHA], game_tree[SCORE])
            if game_tree[ALPHA] >= game_tree[BETA]:
                game_tree[STATE].get_next_player().increment_cutoffs()
                break
    else:  # if game_tree[STATE].next_player == min_player:
        game_tree[SCORE] = math.inf
        children = game_tree[CHILDREN].values()
        if heuristic is not None:
            children = sorted(
                children, key=heuristic)
        for child in children:
            # propagate alpha and beta values to child
            child[ALPHA] = game_tree[ALPHA]
            child[BETA] = game_tree[BETA]
            compute_score(
                game_tree=child,
                max_player=max_player,
                min_player=min_player,
                heuristic=heuristic,
                table=table)
            game_tree[SCORE] = min(game_tree[SCORE], child[SCORE])
            game_tree[BETA] = min(game_tree[BETA], game_tree[SCORE])
            if game_tree[ALPHA] >= game_tree[BETA]:
                game_tree[STATE].get_next_player().increment_cutoffs()
                break

    if table is not None:
        table[table_key] = {
            SCORE: game_tree[SCORE],
            NEXT: game_tree[NEXT]
        }
    return game_tree[SCORE]
