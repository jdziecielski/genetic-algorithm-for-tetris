import copy

import anymino as t
import constants as c


class Shadowmino(t.Anymino):
    def __init__(self, game, shape):
        super().__init__(game)
        self.id = c.BLOCK_COLOR_PENTOMINOS.shadow.value
        self.blocks = []
        if shape is not None:
            for b in shape.blocks:
                self.blocks.append(copy.deepcopy(b))

        self.update_blocks(shape)

    def rotate(self):
        pass

    def find_placement(self):
        can_move = True
        while can_move is True:
            for b in self.blocks:
                if b.y + 1 > c.map_size_y - 1:
                    can_move = False
                    break

            down_most_blocks = self.get_down_most_block()
            for b in down_most_blocks:
                if b.y >= c.map_size_y - 1 or self.game.map_placed_blocks[b.y + 1][b.x] != 0:
                    can_move = False
                    break

            if can_move:
                for b in self.blocks:
                    b.y += 1

    def update_blocks(self, shape):
        if shape is not None:
            for i in range(len(shape.blocks)):
                self.blocks[i].x = shape.blocks[i].x
                self.blocks[i].y = shape.blocks[i].y

            self.find_placement()
