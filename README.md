# Abalone AI

This projects contains several agents to play abalone on the seahorse platform.

Algorithms implemented:

[x] Minimax
[x] AB pruning
[x] AB pruning with nodes sorted by heuristic
[ ] AB pruning with Transposition Table
[ ] AB pruning with Iterative Deepening (and TT)

Heuristics available:

[x] Distance to center of the board
[x] Ejected pieces with distance as a tie-breaker
[ ] Maximise push and ejections available

## Using a heuristic for sorted AB pruning

1. Subclass `MyPlayer` from `my_player_ab` module.
2. Define the heuristic as a scalar function of a `GameState` in one of the following places:
    - as the `self.heuristic` attribute in the `__init__` method
    - if your heuristic depends on element unkown at time of `__init__`,
        override the `get_heuristic` method to create the heuristic using the first `GameState`

