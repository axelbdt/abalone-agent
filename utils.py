from math import inf


def manhattanDist(A, B):
    dist = abs(B[0] - A[0]) + abs(B[1] - A[1])
    return dist


def compute_winner(state):
    """
    Computes the winners of the game based on the scores.

    Args:
        scores (Dict[int, float]): Score for each player

    Returns:
        Iterable[Player]: List of the players who won the game
    """
    scores = state.scores
    max_val = max(scores.values())
    players_id = list(filter(lambda key: scores[key] == max_val, scores))
    itera = list(filter(lambda x: x.get_id()
                 in players_id, state.get_players()))
    if len(itera) > 1:  # égalité
        dist = compute_distances_to_center(state)
        min_dist = min(dist.values())
        players_id = list(filter(lambda key: dist[key] == min_dist, dist))
        itera = list(filter(lambda x: x.get_id()
                     in players_id, state.get_players()))

    if len(itera) > 1:
        return None

    if len(itera) == 1:
        return itera[0]


def compute_terminal_state_score(state, max_player):
    """
    Computes the score of the state for the max_player
    """
    winner = compute_winner(state)
    if winner is None:
        return 0
    if winner.get_id() == max_player.get_id():
        return inf
    else:
        return -inf


def compute_distances_to_center(state):
    """
    compute the distance to center for each player
    return a dict with player_id as key and distance as value
    """
    players_id = [player.get_id() for player in state.get_players()]
    final_rep = state.get_rep()
    env = final_rep.get_env()
    dim = final_rep.get_dimensions()
    dist = dict.fromkeys(players_id, 0)
    center = (dim[0]//2, dim[1]//2)
    for i, j in list(env.keys()):
        p = env.get((i, j), None)
        if p.get_owner_id():
            dist[p.get_owner_id()] += manhattanDist(center, (i, j))
    return dist


def distance_to_center(state, player_id):
    """
    distance to center for the player with player_id
    """
    dist = compute_distances_to_center(state)
    return dist[player_id]


def score(state, player_id):
    """
    Computes the score of the state for the max_player
    """
    return state.scores[player_id]
