import anymino as t
import constants as c
import block as b

class PentominoX(t.Anymino):
    def __init__(self, game):
        super().__init__(game)
        self.id = c.BLOCK_COLOR_PENTOMINOS.X.value
        self.blocks = [b.Block(self.starting_point[0], self.starting_point[1]),
                       b.Block(self.starting_point[0], self.starting_point[1] + 1),
                       b.Block(self.starting_point[0], self.starting_point[1] - 1),
                       b.Block(self.starting_point[0] + 1, self.starting_point[1]),
                       b.Block(self.starting_point[0] - 1, self.starting_point[1])]
        self.states = [[[0, 0], [0, 0], [0, 0], [0, 0]]]
        self.rotation = 0
        self.rotational_block = 0
    def rotate(self):
        pass