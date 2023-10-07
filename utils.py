from typing import Dict


def manhattanDist(A, B):
    dist = abs(B[0] - A[0]) + abs(B[1] - A[1])
    return dist


def compute_score(state, max_player, scores: Dict[int, float]) -> int:
    """
    Computes the winners of the game based on the scores.

    Args:
        scores (Dict[int, float]): Score for each player

    Returns:
        Iterable[Player]: List of the players who won the game
    """
    max_val = max(scores.values())
    players_id = list(filter(lambda key: scores[key] == max_val, scores))
    itera = list(filter(lambda x: x.get_id()
                 in players_id, state.get_players()))
    if len(itera) > 1:  # égalité
        dist = compute_distance_to_center(state, players_id)
        min_dist = min(dist.values())
        players_id = list(filter(lambda key: dist[key] == min_dist, dist))
        itera = list(filter(lambda x: x.get_id()
                     in players_id, state.get_players()))

    if len(itera) > 1:
        return 0

    if len(itera) == 1:
        if itera[0] == max_player:
            return 1
        else:
            return -1


def compute_distance_to_center(state, players_id):
    """
    compute the distance to center for each player
    return a dict with player_id as key and distance as value
    """
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


def distance_to_center(state, player_ids, player_id):
    """
    distance to center for the player with player_id
    takes player_ids as argument probably bc bad design
    TODO: fix the need for player_ids
    """
    dist = compute_distance_to_center(state, player_ids)
    return dist[player_id]
