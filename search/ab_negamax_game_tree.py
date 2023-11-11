from utils import compute_terminal_state_score, compute_normalized_distances_to_center
from keys import STATE, ACTION, SCORE, CHILDREN, ALPHA, BETA, TURN, NEXT, DEPTH, PLAYER
from math import inf
import time


def compute_state_score(state, depth, heuristic, table, quiescence_test=None, alpha=-inf, beta=inf):
    endgame = state.step + depth > state.max_step
    table_key = (state.rep, endgame)
    lookup_result = table.get(table_key)
    if lookup_result is not None and lookup_result[DEPTH] >= depth:
        score = lookup_result[SCORE] if lookup_result[PLAYER] == state.get_next_player() else -lookup_result[SCORE]
        state.get_next_player().increment_successful_lookups()
        return score
    elif state.is_done():
        score = compute_terminal_state_score(
            state)
        depth = inf
    elif depth == 0:
        if quiescence_test is None or quiescence_test(state):
            score = heuristic(state)
        else:
            score = compute_state_score(
                    state,
                    depth=1,
                    heuristic=heuristic,
                    table=table,
                    quiescence_test=None,
                    alpha=-beta,
                    beta=-alpha)
    else:
        score = -inf
        children = sorted(
                state.get_possible_actions(),
                key=lambda x :
                    compute_state_score(
                        x.get_next_game_state(),
                        depth=0,
                        heuristic=heuristic,
                        table=table,
                        quiescence_test=quiescence_test,
                        alpha=-beta,
                        beta=-alpha),
                )
        for child in children:
            child_score = compute_state_score(
                    child.get_next_game_state(),
                    depth=depth-1,
                    heuristic=heuristic,
                    table=table,
                    quiescence_test=quiescence_test,
                    alpha=-beta,
                    beta=-alpha
                )
            score = max(score, -child_score)
            alpha = max(alpha, score)
            if alpha >= beta:
                state.get_next_player().increment_cutoffs()
                break

    table[table_key] = {
        SCORE: score,
        DEPTH: depth,
        PLAYER: state.get_next_player()
    }

    return score
