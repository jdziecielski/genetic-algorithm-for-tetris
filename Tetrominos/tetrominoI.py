import anymino as t
import constants as c
import block as b


class TetrominoI(t.Anymino):
    def __init__(self, game):
        super().__init__(game)
        self.id = c.BLOCK_COLOR_TETROMINOS.I.value
        self.blocks = [b.Block(self.starting_point[0], self.starting_point[1]),
                       b.Block(self.starting_point[0], self.starting_point[1] + 1),
                       b.Block(self.starting_point[0], self.starting_point[1] + 2),
                       b.Block(self.starting_point[0], self.starting_point[1] + 3)]
        self.rotation = c.ROTATIONS.state_2.value
        self.states = [[[-1, 0], [0, -1], [1, 0], [2, 0]],
                       [[0, -1], [1, 0], [0, 1], [0, 2]],
                       [[1, 0], [0, 1], [-1, 0], [-2, 0]],
                       [[0, 1], [-1, 0], [0, -1], [0, -2]]]
        self.rotational_block = 1  # main block for rotation
