
import math
from utils import compute_terminal_state_score
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

    max_player.computed_nodes += 1

    if game_tree[STATE].is_done():
        game_tree[SCORE] = compute_terminal_state_score(
            game_tree[STATE],
            max_player)
        return game_tree[SCORE]

    if game_tree[STATE].next_player == max_player:
        game_tree[SCORE] = -math.inf
        # TODO keep sorted children in game_tree
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
                break
        return

    if game_tree[STATE].next_player == min_player:
        game_tree[SCORE] = math.inf
        # TODO keep sorted children in game_tree
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
                break
        return
