from utils import compute_terminal_state_score, compute_normalized_distances_to_center, push_happened
from keys import STATE, ACTION, SCORE, CHILDREN, ALPHA, BETA, TURN, NEXT, DEPTH, PLAYER
from math import inf
import time

def lookup_score(state, depth, table):
    endgame = state.step + depth > state.max_step
    table_key = (str(state.rep), endgame)
    lookup_result = table.get(table_key)
    if lookup_result is not None and lookup_result[DEPTH] >= depth:
        score = lookup_result[SCORE] if lookup_result[PLAYER] == state.get_next_player() else -lookup_result[SCORE]
        state.get_next_player().increment_successful_lookups()
        return table_key, score
    return table_key, None

def compute_state_score(
        *,
        state,
        depth,
        heuristic,
        table,
        quiescence_test,
        previous_state,
        quiescence_search_depth=2,
        alpha=-inf,
        beta=inf):

    # Lookup in transposition table
    table_key, lookup_result = lookup_score(state, depth, table)
    if lookup_result is not None:
        score = lookup_result
    elif state.is_done():
        # Terminal state
        score = compute_terminal_state_score(
            state)
        depth = inf
    elif depth == 0:
        # Non-terminal state at max depth
        # use quiescence search if a piece was just pushed
        if quiescence_test and push_happened(state, previous_state):
            score = compute_state_score(
                    state=state,
                    depth=quiescence_search_depth,
                    heuristic=heuristic,
                    table=table,
                    previous_state=previous_state,
                    quiescence_test=False,
                    quiescence_search_depth=quiescence_search_depth,
                    alpha=-beta,
                    beta=-alpha)
        else:
            score = heuristic(state)
    else:
        # Non-terminal state at non-max depth
        score = -inf
        children = state.get_possible_actions()
        for child in children:
            child_score = compute_state_score(
                    state=child.get_next_game_state(),
                    depth=depth-1,
                    heuristic=heuristic,
                    table=table,
                    previous_state=state,
                    quiescence_test=quiescence_test,
                    quiescence_search_depth=quiescence_search_depth,
                    alpha=-beta,
                    beta=-alpha
                )
            score = max(score, -child_score)
            alpha = max(alpha, score)
            if alpha >= beta:
                state.get_next_player().increment_cutoffs()
                break

    
    # Update transposition table
    table[table_key] = {
        SCORE: score,
        DEPTH: depth,
        PLAYER: state.get_next_player()
    }

    return score
