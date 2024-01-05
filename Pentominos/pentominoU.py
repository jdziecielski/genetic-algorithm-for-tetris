import anymino as t
import constants as c
import block as b


class PentominoU(t.Anymino):
    def __init__(self, game):
        super().__init__(game)
        self.id = c.BLOCK_COLOR_PENTOMINOS.U.value
        self.blocks = [b.Block(self.starting_point[0], self.starting_point[1]),
                       b.Block(self.starting_point[0] - 1, self.starting_point[1]),
                       b.Block(self.starting_point[0] + 1, self.starting_point[1]),
                       b.Block(self.starting_point[0] - 1, self.starting_point[1] + 1),
                       b.Block(self.starting_point[0] + 1, self.starting_point[1] + 1)]
        self.rotational_block = 0  # main block for rotation
        self.rotation = c.ROTATIONS.state_1.value
        self.states = [[[0, 0], [-1, 0], [1, 0], [-1, 1], [1, 1]],
                       [[0, 0], [0, -1], [0, 1], [-1, -1], [-1, 1]],
                       [[0, 0], [-1, 0], [1, 0], [-1, -1], [1, -1]],
                       [[0, 0], [0, -1], [0, 1], [1, -1], [1, 1]]]
