from typing import Dict, Iterable, List
from collections import Counter

from seahorse.game.game_state import GameState
from seahorse.game.master import GameMaster
from seahorse.player.player import Player


class MasterAbalone(GameMaster):
    """
    Master to play the game Abalone

    Attributes:
        name (str): Name of the game
        initial_game_state (GameState): Initial state of the game
        current_game_state (GameState): Current state of the game
        players_iterator (Iterable): An iterable for the players_iterator, ordered according to the playing order.
            If a list is provided, a cyclic iterator is automatically built
        log_level (str): Name of the log file
    """

    def __init__(self, name: str, initial_game_state: GameState, players_iterator: Iterable[Player], log_level: str, port: int = 8080, hostname: str = "localhost") -> None:
        super().__init__(name, initial_game_state, players_iterator, log_level, port, hostname)
        
    def compute_winner(self, scores: Dict[int, float]) -> List[Player]:
        """
        Computes the winners of the game based on the scores.

        Args:
            scores (Dict[int, float]): Score for each player

        Returns:
            Iterable[Player]: List of the players who won the game
        """
        def manhattanDist(A, B):
            mask1 = [(0,2),(1,3),(2,4)]
            mask2 = [(0,4)]
            diff = (abs(B[0] - A[0]),abs(B[1] - A[1]))
            dist = (abs(B[0] - A[0]) + abs(B[1] - A[1]))/2
            if diff in mask1:
                dist += 1
            if diff in mask2:
                dist += 2
            return dist
        
        max_val = max(scores.values())
        players_id = list(filter(lambda key: scores[key] == max_val, scores))
        itera = list(filter(lambda x: x.get_id() in players_id, self.players))
        if len(itera) > 1: #égalité
            final_rep = self.current_game_state.get_rep()
            env = final_rep.get_env()
            dim = final_rep.get_dimensions()
            dist = dict.fromkeys(players_id, 0)
            center = (dim[0]//2, dim[1]//2)
            for i, j in list(env.keys()):
                p = env.get((i, j), None)
                if p.get_owner_id():
                    dist[p.get_owner_id()] += manhattanDist(center, (i, j))
            min_dist = min(dist.values())
            players_id = list(filter(lambda key: dist[key] == min_dist, dist))
            itera = list(filter(lambda x: x.get_id() in players_id, self.players))
        return itera
