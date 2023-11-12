from math import inf
import copy


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


## Distance to center heuristic

def compute_normalized_distances_to_center(state):
    """
    Compute the distance to center for each player
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


## Adjacency heuristic

def get_adjacency(state, player):
    """
    Computes the adjacency between all the marbles for a player:
    normalized to be lower than 1 so that score remains more important
    return a dict with player_id as key and distance as value
    """
    pieces_pos = state.get_rep().get_pieces_player(player)[1]
    neighbourhood_scores = []
    max_piece_score = len(state.get_neighbours(pieces_pos[0][0], pieces_pos[0][1]))
    for piece in pieces_pos:
        neighbours = state.get_neighbours(piece[0], piece[1])
        piece_score = 0
        for key in neighbours:
            # Reduce score if the marble is near an edge
            if neighbours[key][0] == "OUTSIDE":
                piece_score -= 1
            # Augment score if the marble is part of a group
            elif neighbours[key][0] == player.get_piece_type():
                piece_score += 1
        neighbourhood_scores.append(piece_score / max_piece_score)
    adjacency_score = sum(neighbourhood_scores) / len(neighbourhood_scores)
    return adjacency_score

def heuristic_adjacency(state):
    """
    Compute the adjacency between players' marbles
    """
    # Get players id
    opponent = state.get_next_player()
    opponent_id = opponent.get_id()
    player = get_opponent(state, opponent)
    player_id = player.get_id()

    adjacency_scores = {player_id: get_adjacency(state, player),
                        opponent_id: get_adjacency(state, opponent)}
    return adjacency_scores


## Pushes and ejections heuristic

def get_avg_pushes(state, opponent):
    """
    Computes the average number of pushes available in this state for the player
    by checking the differences in the positions of the player's pieces between 
    this state and the next ones.
    TODO: involves checking another level deep for both players so it's quite slow (O(n^2)?)
    TODO: more efficient version by only computing places where a player outnumbers its opponent?
    """
    # Get the previous positions of the given player's pieces and their number
    prev_nb, prev_pos = state.get_rep().get_pieces_player(opponent)

    nb_pushes_list = []

    # Check for each action if there are possible pushes
    # i.e., changes in the next player's positions
    for move in state.get_possible_actions():
        new_state = move.get_next_game_state()
        
        # Differences in the positions of the given player's pieces
        new_nb, new_pos = new_state.get_rep().get_pieces_player(opponent)
        differences = set(new_pos).symmetric_difference(set(prev_pos))
        
        # Add the number of pieces pushed for this action
        # normalized by the maximum number of pieces pushed (2)
        nb_pushes = len(differences) / 2

        # Count the number of ejections
        nb_ejections = prev_nb - new_nb

        # Define a ratio to ponder the pushes and ejections (ejections should be more important)
        push_ratio = 0.2
        nb_pushes_list.append(push_ratio*nb_pushes + (1-push_ratio)*nb_ejections)

    # Get the average number of marbles pushed with actions possible from this state
    nb_pushes_avg = 0
    if len(nb_pushes_list) != 0:
        nb_pushes_avg += sum(nb_pushes_list) / len(nb_pushes_list)
    
    return nb_pushes_avg

def heuristic_push(state):
    """
    Compute how many opponent's marbles can be pushed by moving (pressure)
    TODO: Weigh the score so that an ejection is more important than just pushing
    In game: if it's possible to move
    or
    In next state: the opponent's marbles will have moved
    ==> Check in next node if the score changes for ejections
    Normalized by the number of possible actions?
    """
    # Get players' ids
    opponent = state.get_next_player()
    opponent_id = opponent.get_id()
    player = get_opponent(state, opponent)
    player_id = player.get_id()

    # The next player in the state is the opponent because the player has just moved
    # View the state as if the player was playing again to see how it can push from this new positions
    state_from_player = copy.deepcopy(state)
    state_from_player.next_player = state_from_player.compute_next_player()

    nb_pushes_avg = {player_id: get_avg_pushes(state_from_player, opponent), 
                     opponent_id: get_avg_pushes(state, player)}

    return nb_pushes_avg


def get_pushes2(state):
    player = state.get_next_player()
    opponent = get_opponent(state, player)
    opponent_positions = set(state.get_rep().get_pieces_player(opponent)[1])

    pushes = sum(len(opponent_positions -
                     set(action.get_next_game_state().get_rep().get_pieces_player(opponent)[1]))
                  for action in state.get_possible_actions())
    return pushes

def push_happened(state, previous_state):
    """
    Checks if a push happened between the previous state and the current state
    """
    player = state.get_next_player()
    # Get the previous positions of the given player's pieces
    prev_pos = previous_state.get_rep().get_pieces_player(player)[1]

    # Differences in the positions of the given player's pieces
    new_pos = state.get_rep().get_pieces_player(player)[1]
    return not (set(new_pos) == set(prev_pos))


## Combination of the heuristics  

def score_and_distance_sym(state):
    # TODO: find better name
    """
    Combines score and distance to center for an heuristic
    that would give the winner of the game
    """
    scores = state.scores
    player = state.get_next_player()
    opponent = get_opponent(state, player)
    # opponent = state.get_next_player()
    # player = get_opponent(state, opponent)
    player_id = player.get_id()
    opponent_id = opponent.get_id()
    dist = compute_normalized_distances_to_center(state)
    score_and_dist = scores[player_id] - dist[player_id]
    opponent_score_and_dist = scores[opponent_id] - dist[opponent_id]
    result = score_and_dist - opponent_score_and_dist
    return result


def heuristic_combined(state, heuristics_used):
    """
    Combines the different heuristics with weights
    - True score (i.e. ejections)
    - Normalized distance to center
    - Possible pushes
    - Adjacency of the marbles
    for a heuristic that would give the winner of the game
    """
    # Extraction of the players' information
    player = state.get_next_player()
    opponent = get_opponent(state, player)
    player_id = player.get_id()
    opponent_id = opponent.get_id()

    # Initialisation of the players' scores
    h_player = 0
    h_opponent = 0
    
    if "score" in heuristics_used:
        scores = state.scores
        h_player += heuristics_used["score"] * scores[player_id]
        h_opponent += heuristics_used["score"] * scores[opponent_id]
    
    if "center" in heuristics_used:
        dist_to_center = compute_normalized_distances_to_center(state)
        h_player -= heuristics_used["center"] * dist_to_center[player_id]
        h_opponent -= heuristics_used["center"] * dist_to_center[opponent_id]
    
    if "push" in heuristics_used:
        pushes = heuristic_push(state)
        h_player += heuristics_used["push"] * pushes[player_id]
        h_opponent += heuristics_used["push"] * pushes[opponent_id]
    
    if "adjacency" in heuristics_used:
        pushes = heuristic_adjacency(state)
        h_player += heuristics_used["adjacency"] * pushes[player_id]
        h_opponent += heuristics_used["adjacency"] * pushes[opponent_id]
    
    h_sym = h_player - h_opponent
    
    return h_sym









#######################################################################################

## USELESS?

## Score heuristic

# It is not used anywhere

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


def compute_terminal_state_score(state):
    """
    Computes the score of the state for the max_player
    """
    winner = compute_winner(state)
    if winner is None:
        return 0
    if winner.get_id() == state.get_next_player().get_id():
        return inf
    else:
        return -inf


def score(state, player_id):
    """
    Computes the score of the state for the max_player
    """
    return state.scores[player_id]



## There is a normalized version
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


