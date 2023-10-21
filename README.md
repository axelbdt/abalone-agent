# Abalone AI

This projects contains several agents to play abalone on the seahorse platform.

Algorithms implemented:

- [x] Minimax
- [x] AB pruning
- [x] AB pruning with nodes sorted by heuristic
- [ ] AB pruning with Transposition Table
- [ ] AB pruning with Iterative Deepening (and TT)

Heuristics available:

- [x] Distance to center of the board
- [x] Ejected pieces with distance as a tie-breaker
- [ ] Maximise push and ejections available

## Run the agents

Run once:
```
python main_abalone.py -g -c simplified -t local my_player_ab_distance.py random_player_abalone.py 
```

More info on options with `python main_abalone.py -h`.

Run on every file change with watchexec:
```
watchexec -e py -- python main_abalone.py -g -c simplified -t local my_player_ab_distance.py random_player_abalone.py 
```

### Smaller games

#### Simplified config

In addition to `classical` and `alien` starting position,
there is an additionnal `simplified` config where each player has 3 pieces available.

#### Shorter games

To limit the number of turns, change `MAX_STEP` value in `constants` module.

To limit the goal score, change `MAX_SCORE` value in `constants` module.

## Measure agent performance

Beside victory, an agent logs the following info :

- Time remaining at the end of the game
- Nodes where score was computed (as terminal node or from children)
- (for agents with a Transposition Table) the number of successful lookups

## Using a heuristic for sorted AB pruning

1. Subclass `MyPlayer` from `ab` module.
2. Define the heuristic as a scalar function of a `GameState` in one of the following places:
    - as the `self.heuristic` attribute in the `__init__` method
    - if your heuristic depends on element unkown at time of `__init__`,
        override the `get_heuristic` method to create the heuristic using the first `GameState`

