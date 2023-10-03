from __future__ import annotations
from typing import Any, List, Tuple

import json
from typing import Dict
from seahorse.game.game_layout.board import Board, Piece
from seahorse.utils.serializer import Serializable


class BoardAbalone(Board):
    """
    A class representing an Abalone board.

    Attributes:
        env (dict[Tuple[int], Piece]): The environment dictionary composed of pieces.
        dimensions (list[int]): The dimensions of the board.
    """

    EMPTY_POS=3
    FORBIDDEN_POS=0

    FORBIDDEN_MASK = [
     [True,  True,  True,  True,  False, True,  True,  True,  True],
     [True,  True,  True,  False, True,  False, True,  True,  True],
     [True,  True,  False, True,  False, True,  False, True,  True],
     [True,  False, True,  False, True,  False, True,  False, True],
     [False, True,  False, True,  False, True,  False, True,  False],
     [True,  False, True,  False, True,  False, True,  False, True],
     [False, True,  False, True,  False, True,  False, True,  False],
     [True,  False, True,  False, True,  False, True,  False, True],
     [False, True,  False, True,  False, True,  False, True,  False],
     [True,  False, True,  False, True,  False, True,  False, True],
     [False, True,  False, True,  False, True,  False, True,  False],
     [True,  False, True,  False, True,  False, True,  False, True],
     [False, True,  False, True,  False, True,  False, True,  False],
     [True,  False, True,  False, True,  False, True,  False, True],
     [True,  True,  False, True,  False, True,  False, True,  True],
     [True,  True,  True,  False, True,  False, True,  True,  True],
     [True,  True,  True,  True,  False, True,  True,  True,  True],
    ]

    def __init__(self, env: dict[tuple[int], Piece], dim: list[int]) -> None:
        super().__init__(env, dim)

    def __str__(self) -> str:
        """
        Return a string representation of the board.

        Returns:
            str: The string representation of the board.
        """
        grid_data=self.get_grid()
        string = ""
        for i in range(9):
            if i % 2 == 1:
                string += " "
            for j in range(9):
                if grid_data[i][j] == BoardAbalone.FORBIDDEN_POS:
                    string += "  "
                elif grid_data[i][j] == BoardAbalone.EMPTY_POS:
                    string += "_ "
                else:
                    string += str(grid_data[i][j]) + " "
            string += "\n"
        return string
    
    def get_neighbours(self, i:int ,j: int) -> Dict[str,Tuple[str,Tuple[int,int]]]:
        """ returns a dictionnary of the neighbours of the cell (i,j) with the following format:
            
        (neighbour_name: (neighbour_type, (i,j)))


        Args:
            i (int): line indice
            j (int): column indice

        Returns:
            Dict[str,Tuple[str,Tuple[int,int]]]: dictionnary of the neighbours of the cell (i,j)
        """
        neighbours = {"top_left":(i-1,j-1), "top_right":(i-2,j), "left":(i+1,j-1), "right":(i-1,j+1), "bottom_left":(i+2,j), "bottom_right":(i+1,j+1)}
        for k,v in neighbours.items():
            if v not in self.env.keys():
                if v[0] < 0 or v[1] < 0 or v[0] >= self.dimensions[0] or v[1] >= self.dimensions[1]:
                    neighbours[k] = ("OUTSIDE",neighbours[k])
                else:
                    if BoardAbalone.FORBIDDEN_MASK[v[0]][v[1]]:
                        neighbours[k] = ("OUTSIDE",neighbours[k])
                    else:
                        neighbours[k] = ("EMPTY",neighbours[k])
            else:
                neighbours[k] = (self.env[neighbours[k]].get_type(),neighbours[k])
        return neighbours

    def get_grid(self) -> List[List[int]]:
        """
        Return a nice representation of the board.

        Returns:
            str: The nice representation of the board.
        """
        grid_data = [
            [0, 0, 2, 2, 2, 2, 2, 0, 0],
            [0, 2, 2, 2, 2, 2, 2, 0, 0],
            [0, 3, 3, 2, 2, 2, 3, 3, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 0],
            [0, 3, 3, 1, 1, 1, 3, 3, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0],
        ]
        positions = [
            ((0, 6), (0, 4)), ((0, 5), (1, 3)), ((0, 4), (2, 2)),
            ((0, 3), (3, 1)), ((0, 2), (4, 0)), ((1, 6), (1, 5)),
            ((1, 5), (2, 4)), ((1, 4), (3, 3)), ((1, 3), (4, 2)),
            ((1, 2), (5, 1)), ((1, 1), (6, 0)), ((2, 7), (2, 6)),
            ((2, 6), (3, 5)), ((2, 5), (4, 4)), ((2, 4), (5, 3)),
            ((2, 3), (6, 2)), ((2, 2), (7, 1)), ((2, 1), (8, 0)),
            ((3, 7), (3, 7)), ((3, 6), (4, 6)), ((3, 5), (5, 5)),
            ((3, 4), (6, 4)), ((3, 3), (7, 3)), ((3, 2), (8, 2)),
            ((3, 1), (9, 1)), ((4, 8), (4, 8)), ((4, 7), (5, 7)),
            ((4, 6), (6, 6)), ((4, 5), (7, 5)), ((4, 4), (8, 4)),
            ((4, 3), (9, 3)), ((5, 7), (6, 8)), ((5, 6), (7, 7)),
            ((5, 5), (8, 6)), ((5, 4), (9, 5)), ((6, 7), (8, 8)),
            ((6, 6), (9, 7)), ((5, 3), (10, 4)), ((5, 2), (11, 3)),
            ((5, 1), (12, 2)), ((5, 0), (13, 1)), ((4, 2), (10, 2)),
            ((4, 1), (11, 1)), ((4, 0), (12, 0)), ((6, 5), (10, 6)),
            ((6, 4), (11, 5)), ((6, 3), (12, 4)), ((6, 2), (13, 3)),
            ((6, 1), (14, 2)), ((7, 6), (10, 8)), ((7, 5), (11, 7)),
            ((7, 4), (12, 6)), ((7, 3), (13, 5)), ((7, 2), (14, 4)),
            ((7, 1), (15, 3)), ((8, 6), (12, 8)), ((8, 5), (13, 7)),
            ((8, 4), (14, 6)), ((8, 3), (15, 5)), ((8, 2), (16, 4)),
            ((3, 0), (10, 0))
        ]

        for x,y in positions:
            grid_data[x[0]][x[1]] = self.get_env().get(y).get_type() if  self.get_env().get(y) else BoardAbalone.EMPTY_POS

        return grid_data

    def to_json(self) -> dict:
        """
        Converts the board to a JSON object.

        Returns:
            dict: The JSON representation of the board.
        """
        # TODO: migrate below into js code
        #board = [[None for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])]
        #for key, value in self.env.items():
        #    board[key[0]][key[1]] = value.piece_type if value is not None else None
        #return {"board": board}
        return {"env":{str(x):y for x,y in self.env.items()},"dim":self.dimensions}

    @classmethod
    def from_json(cls, data) -> Serializable:
        d = json.loads(data)
        dd = json.loads(data)
        for x,y in d["env"].items():
            # TODO eval is unsafe
            del dd["env"][x]
            dd["env"][eval(x)] = Piece.from_json(json.dumps(y))
        return cls(**dd)

