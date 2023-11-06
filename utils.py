from math import inf


def manhattanDist(A, B):
    mask1 = [(0, 2), (1, 3), (2, 4)]
    mask2 = [(0, 4)]
    diff = (abs(B[0] - A[0]), abs(B[1] - A[1]))
    dist = (abs(B[0] - A[0]) + abs(B[1] - A[1]))/2
    if diff in mask1:
        dist += 1
    if diff in mask2:
        dist += 2
    return dist


def get_opponent(state, player):
    """
    Returns the opponent of the player supplied as argument
    """
    players = state.get_players()
    opponent = (players[1] if players[0] == player
                else players[0])
    return opponent



## Score heuristic


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


def score(state, player_id):
    """
    Computes the score of the state for the max_player
    """
    return state.scores[player_id]



## Distance to center heuristic


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


def compute_normalized_distances_to_center(state):
    """
    compute the distance to center for each player
    normalized to be lower than 1 so that score remains more important
    return a dict with player_id as key and distance as value
    """
    players_id = [player.get_id() for player in state.get_players()]
    final_rep = state.get_rep()
    env = final_rep.get_env()
    dim = final_rep.get_dimensions()
    dist = dict.fromkeys(players_id, 0)
    pieces = dict.fromkeys(players_id, 0)
    center = (dim[0]//2, dim[1]//2)
    for i, j in list(env.keys()):
        p = env.get((i, j), None)
        if p.get_owner_id():
            # divide distance by 5 as the max distance is 4
            dist[p.get_owner_id()] += manhattanDist(center, (i, j)) / 5
            pieces[p.get_owner_id()] += 1
    for player_id in players_id:
        dist[player_id] /= pieces[player_id]
    return dist


def score_and_distance(state, player_id, opponent_id):
    """
    Combines score and distance to center for an heuristic
    that would give the winner of the game
    """
    scores = state.scores
    dist = compute_normalized_distances_to_center(state)
    score_and_dist = scores[player_id] - dist[player_id]
    opponent_score_and_dist = scores[opponent_id] - dist[opponent_id]
    return score_and_dist - opponent_score_and_dist


def score_and_distance_sym(state):
    # TODO: find better name
    """
    Combines score and distance to center for an heuristic
    that would give the winner of the game
    """
    scores = state.scores
    # player_id = state.get_next_player().get_id()
    # opponent_id = get_opponent(state, player_id).get_id()
    opponent = state.get_next_player()
    opponent_id = opponent.get_id()
    player_id = get_opponent(state, opponent).get_id()
    dist = compute_normalized_distances_to_center(state)
    score_and_dist = scores[player_id] - dist[player_id]
    opponent_score_and_dist = scores[opponent_id] - dist[opponent_id]
    result = score_and_dist - opponent_score_and_dist
    return result



## Adjacency heuristic


# def compute_cohesion(state):
#     """
#     Compute the distance between all the marbles for a player
#     normalized to be lower than 1 so that score remains more important
#     return a dict with player_id as key and distance as value
#     """
#     players_id = [player.get_id() for player in state.get_players()]
#     final_rep = state.get_rep()
#     env = final_rep.get_env()
#     dim = final_rep.get_dimensions()
#     coords = dict.fromkeys(players_id, [])
#     dist = dict.fromkeys(players_id, 0)
#     pieces = dict.fromkeys(players_id, 0)
#     center = (dim[0]//2, dim[1]//2)
#     # Get the coordinates of the pieces left for each player
#     for i, j in list(env.keys()):
#         p = env.get((i, j), None)
#         if p.get_owner_id():
#             coords[p.get_owner_id()].append((i, j))
#             pieces[p.get_owner_id()] += 1
#     # Calculate the sum of the distances of all the pieces to their barycentre
#     for player_id in players_id:
#         center = tuple([sum(c) / len(c) for c in zip(*coords[player_id])])
#         for piece in coords[player_id]:
#             # divide distance by 5 as the max distance is 4
#             dist[player_id] += manhattanDist(center, piece) / 5
#         dist[player_id] /= pieces[player_id]
#     return dist


# def score_and_distance_and_cohesion_sym(state):
#     # TODO: find better name
#     """
#     Combines score and distance to center for an heuristic
#     that would give the winner of the game
#     """
#     scores = state.scores
#     opponent = state.get_next_player()
#     opponent_id = opponent.get_id()
#     player_id = get_opponent(state, opponent).get_id()
#     dist = compute_normalized_distances_to_center(state)
#     dist_cohesion = compute_cohesion(state)
#     score_and_dist = scores[player_id] - dist[player_id] - dist_cohesion[player_id]
#     opponent_score_and_dist = scores[opponent_id] - dist[opponent_id] - dist_cohesion[opponent_id]
#     result = score_and_dist - opponent_score_and_dist
#     return result


def get_adjacency_score(state, player):
    pieces_pos = state.get_rep().get_pieces_player(player)[1]
    neighbourhood_scores = []
    max_piece_score = len(state.get_neighbours(pieces_pos[0][0], pieces_pos[0][1]))
    for piece in pieces_pos:
        neighbours = state.get_neighbours(piece[0], piece[1])
        piece_score = 0
        for key in neighbours:
            if neighbours[key][0] == "OUTSIDE":
                piece_score -= 1
            elif neighbours[key][0] == player.get_piece_type():
                piece_score += 1
        neighbourhood_scores.append(piece_score / max_piece_score)
    adjacency_score = sum(neighbourhood_scores) / len(neighbourhood_scores)
    return adjacency_score


def get_adjacency(state):
    """
    Compute the adjacency between players' marbles
    """
    # Get players id
    opponent = state.get_next_player()
    opponent_id = opponent.get_id()
    player = get_opponent(state, opponent)
    player_id = player.get_id()

    adjacency_scores = {player_id: get_adjacency_score(state, player),
                        opponent_id: get_adjacency_score(state, opponent)}
    return adjacency_scores


def score_distance_adjacency(state):
    """
    Combines score, distance to center and adjacency for a heuristic
    that would give the winner of the game
    """
    # coefs = (1e2, 1e1, 1e0)
    
    # Get players' ids
    opponent = state.get_next_player()
    opponent_id = opponent.get_id()
    player_id = get_opponent(state, opponent).get_id()

    scores = state.scores
    dist = compute_normalized_distances_to_center(state)
    # dist_cohesion = compute_cohesion(state)
    # push = get_pushes(state)
    adjacency = get_adjacency(state)
    
    score_player = scores[player_id] - dist[player_id] + 0.1*adjacency[player_id]  # - dist_cohesion[player_id] + push[player_id]
    score_opponent = scores[opponent_id] - dist[opponent_id] + 0.1*adjacency[opponent_id]  # - dist_cohesion[opponent_id] + push[opponent_id]
    result = score_player - score_opponent

    return result



## Pushes and ejections heuristic


# # By checking changes between the current state and the possible next states
# # ==> only goes one level deeper than current state
# # so gives only the average number of pushes available from the current state
# def pushes(state):
#     """
#     Compute how many opponent's marbles can be pushed by moving (pressure)
#     Weigh the score so that an ejection is more important than just pushing
#     In game: if it's possible to move
#     or
#     In next state: the opponent's marbles will have moved
#     ==> Check in next node if the score changes for ejections
#     Normalized by the number of possible actions?
#     """
#     # Get all possible actions from the current state
#     actions = state.get_possible_actions()

#     # Get players' ids
#     opponent = state.get_next_player()
#     opponent_id = opponent.get_id()
#     player_id = get_opponent(state, opponent).get_id()

#     # Check all the next states to see which one averages more possible pushes
#     # i.e., a change in the next player's positions
#     state_dict = state.get_rep().get_env()
#     print("positions:", state.get_rep().get_pieces_player(opponent))
#     nb_pushed_opponent, nb_pushed_player = [], []

#     # Check which possible actions lead to a possible push
#     for move in actions:
#         new_positions = state.get_rep().get_pieces_player(opponent)
#         print("new_positions:", new_positions)

#         new_state_dict = move.get_next_game_state().get_rep().get_env()
#         # Get differences between the two states
#         differences = dict(set(new_state_dict.items()) - set(state_dict.items()))
        
#         pushed_player = list(filter(lambda key: differences[key].get_owner_id() == player_id, differences))
#         nb_pushed_player.append(len(pushed_player))

#         pushed_opponent = list(filter(lambda key: differences[key].get_owner_id() == opponent_id, differences))
#         nb_pushed_opponent.append(len(pushed_opponent))
#     nb_pushes_avg = {player_id: 0, opponent_id: 0}
#     if len(nb_pushed_player) != 0:
#         nb_pushes_avg[player_id] = sum(nb_pushed_player) / len(nb_pushed_player)
#     if len(nb_pushed_opponent):
#         nb_pushes_avg[opponent_id] = sum(nb_pushed_opponent) / len(nb_pushed_opponent)
#     return nb_pushes_avg


# By checking changes between states 
# ==> involves checking 2 levels deep so it's quite slow (O(n^2)?)
def get_avg_pushes(state, player):
    """
    Computes the average number of pushes available in this state for the player
    """
    # Get the previous positions of the given player's pieces
    prev_pos = state.get_rep().get_pieces_player(player)[1]

    nb_pushes = []

    for move in state.get_possible_actions():
        new_state = move.get_next_game_state()

        # Differences in the positions of the given player's pieces
        new_pos = new_state.get_rep().get_pieces_player(player)[1]
        differences = list(set(new_pos) - set(prev_pos))

        # Add the number of moves that can lead to pushed pieces in this new state
        nb_pushes.append(len(differences))

    nb_pushes_avg = sum(nb_pushes) / len(nb_pushes)
    return nb_pushes_avg


def get_pushes(state):
    """
    Compute how many opponent's marbles can be pushed by moving (pressure)
    Weigh the score so that an ejection is more important than just pushing
    In game: if it's possible to move
    or
    In next state: the opponent's marbles will have moved
    ==> Check in next node if the score changes for ejections
    Normalized by the number of possible actions?
    """
    # Get all possible actions from this state
    actions = state.get_possible_actions()

    # Get players id
    opponent = state.get_next_player()
    opponent_id = opponent.get_id()
    player = get_opponent(state, opponent)
    player_id = player.get_id()

    # Check which possible actions lead to a possible push
    # i.e., a change in the next player's positions
    nb_pushed_opponent, nb_pushed_player = [], []

    # For each move
    for move in actions:
        # Get the new state
        new_state = move.get_next_game_state()
        
        # Compute the average number of pushes available from that new state
        nb_pushed_opponent.append(get_avg_pushes(new_state, opponent))
        nb_pushed_player.append(get_avg_pushes(new_state, player))

    nb_pushes_avg = {player_id: 0, opponent_id: 0}
    if len(nb_pushed_player) != 0:
        nb_pushes_avg[player_id] = sum(nb_pushed_player) / len(nb_pushed_player)
    if len(nb_pushed_opponent) != 0:
        nb_pushes_avg[opponent_id] = sum(nb_pushed_opponent) / len(nb_pushed_opponent)

    return nb_pushes_avg


def pressure(state):
    """
    Combines different heuristices with weights:
        # 1. True score
        # 2. Possible ejections
        # 3. Possible pushes (among which there are ejections)
        # 4. Normalized distance to center and distance to center for an heuristic
    """
    # coefs = (1e2, 1e1, 1e0)
    
    # Get players' ids
    opponent = state.get_next_player()
    opponent_id = opponent.get_id()
    player_id = get_opponent(state, opponent).get_id()

    # scores = state.scores
    dist = compute_normalized_distances_to_center(state)
    # dist_cohesion = compute_cohesion(state)
    # push = get_pushes(state)
    adjacency = get_adjacency(state)
    
    score_player = adjacency[player_id] - dist[player_id]  # + scores[player_id] - dist_cohesion[player_id] + push[player_id]
    score_opponent = adjacency[opponent_id] - dist[opponent_id]  # scores[opponent_id] - dist_cohesion[opponent_id] + push[opponent_id]
    result = score_player - score_opponent

    return result
