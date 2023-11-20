# Axel BAUDOT (2297081)
# Thomas PERRIN (2229377)

from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from math import inf
from statistics import fmean

# constants for game tree dict keys
STATE = "state"
ACTION = "action"
DEPTH = "depth"
SCORE = "score"
CHILDREN = "children"
ALPHA = "alpha"
BETA = "beta"
NEXT = "next"
TURN = "turn"
PLAYER = "player"


# constants for info dict keys
COMPUTED_NODES = "computed_nodes"
SUCCESSFUL_LOOKUPS = "successful_lookups"
CUTOFFS = "cutoffs"

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


def get_adjacency(state, player):
    """
    Computes the adjacency between all the marbles for a player:
    normalized to be lower than 1 so that score remains more important
    return a dict with player_id as key and distance as value
    """
    pieces_pos = state.get_rep().get_pieces_player(player)[1]
    neighbourhood_scores = [
        len([_ for _, neighbour in state.get_neighbours(piece[0], piece[1]).items() 
             if neighbour[0] == player.get_piece_type()])
        for piece in pieces_pos
    ]
    adjacency_score = fmean(neighbourhood_scores) / 6
    return adjacency_score

def compute_adjacency(state):
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

def score_distance_adjacency_sym(state):
    """
    Combines score, distance to center and adjacency for an heuristic
    that would give the winner of the game
    """
    scores = state.scores
    player = state.get_next_player()
    opponent = get_opponent(state, player)
    player_id = player.get_id()
    opponent_id = opponent.get_id()
    dist = compute_normalized_distances_to_center(state)
    adjacency = compute_adjacency(state)
    value = combine_heuristics(scores[player_id], dist[player_id], adjacency[player_id])
    opponent_value = combine_heuristics(scores[opponent_id], dist[opponent_id], adjacency[opponent_id])
    result = value - opponent_value
    return result

def combine_heuristics(score, dist, adjacency):
    coeff_score = 10
    coeff_dist = 10
    coeff_adjacency = 1
    return coeff_score * score - coeff_dist * dist + coeff_adjacency * adjacency

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

def lookup_score(state, depth, table):
    endgame = state.step + depth > state.max_step
    table_key = (str(state.rep), endgame)
    lookup_result = table.get(table_key)
    if lookup_result is not None and lookup_result[DEPTH] >= depth:
        score = lookup_result[SCORE] if lookup_result[PLAYER] == state.get_next_player() else -lookup_result[SCORE]
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
        quiescence_search_depth=1,
        alpha=-inf,
        beta=inf):
    """
    Computes the score of the state for using negamax with alpha-beta pruning and transposition table
    """

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
                break

    
    # Update transposition table
    table[table_key] = {
        SCORE: score,
        DEPTH: depth,
        PLAYER: state.get_next_player()
    }

    return score

class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.
    The player will use the alpha-beta pruning algorithm to compute the best action.
    A different heuristic can be provided in subclasses

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float = 60*15, *args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name, time_limit, *args)
        self.game_tree = None
        self.computed_nodes = 0
        self.heuristic = score_distance_adjacency_sym
        self.table = {}
        self.search_depth = 3
        self.quiescence_search_depth = 1
        self.use_quiescence_test = True

    def to_json(self):
        return ""

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        # Play fast if no time left
        if self.get_remaining_time() < 60:
            self.search_depth = 2
            self.use_quiescence_test = False

        # compute score of current state and incidentally the scores of the children
        compute_state_score(
            state=current_state,
            depth = self.search_depth,
            heuristic=self.heuristic,
            table=self.table,
            previous_state=current_state,
            quiescence_search_depth=self.quiescence_search_depth,
            quiescence_test=self.use_quiescence_test)

        # use the transposition table to get the best action
        next_action = max(
                current_state.get_possible_actions(),
                key=lambda x: - (lookup_score(x.get_next_game_state(), -inf, self.table)[1] or inf))

        return next_action
