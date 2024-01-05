import anymino as t
import constants as c
import block as b


class TetrominoJ(t.Anymino):
    def __init__(self, game):
        super().__init__(game)
        self.id = c.BLOCK_COLOR_TETROMINOS.J.value
        self.blocks = [b.Block(self.starting_point[0], self.starting_point[1]),
                       b.Block(self.starting_point[0], self.starting_point[1] + 1),
                       b.Block(self.starting_point[0], self.starting_point[1] + 2),
                       b.Block(self.starting_point[0] - 1, self.starting_point[1] + 2)]
        self.rotation = c.ROTATIONS.state_4.value
        self.states = [[[1, 0], [0, 0], [-1, 0], [-1, -1]],
                       [[0, -1], [0, 0], [0, 1], [1, -1]],
                       [[-1, 0], [0, 0], [1, 0], [1, 1]],
                       [[0, -1], [0, 0], [0, 1], [-1, 1]]]
        self.rotational_block = 1  # main block for rotation