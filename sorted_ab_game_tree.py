import math
from utils import compute_state_score, distance_to_center
from keys import STATE, SCORE, CHILDREN, ALPHA, BETA
from ab_game_tree import expand
from ab_game_tree import create_game_tree as ab_create_game_tree

create_game_tree = ab_create_game_tree


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
        ordered_children = sorted(
            game_tree[CHILDREN].values(),
            key=lambda x: distance_to_center(x[STATE],
                                             [max_player.get_id(),
                                              min_player.get_id()],
                                             max_player.get_id()))

        for child in ordered_children:
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
        ordered_children = sorted(
            game_tree[CHILDREN].values(),
            key=lambda x: distance_to_center(x[STATE],
                                             [max_player.get_id(),
                                              min_player.get_id()],
                                             min_player.get_id()))

        for child in ordered_children:
            # propagate alpha and beta values to child
            child[ALPHA] = game_tree[ALPHA]
            child[BETA] = game_tree[BETA]
            compute_score(child, max_player, min_player)
            game_tree[SCORE] = min(game_tree[SCORE], child[SCORE])
            game_tree[BETA] = min(game_tree[BETA], game_tree[SCORE])
            if game_tree[ALPHA] >= game_tree[BETA]:
                break
        return
