import constants as c
import copy


class Anymino:
    def __init__(self, game):
        self.id = -1
        self.starting_point = c.block_starting_point
        self.blocks = []
        self.rotation = -1
        self.game = game
        self.states = []
        self.rotational_block = None
        self.can_move = True
        self.is_rotation_possible = True

    def move_left(self):
        if self.game.current_shape is not None:
            self.can_move = True
            left_most_blocks = []

            for b in self.blocks:
                left_most_blocks.append(b)
                size = len(left_most_blocks)
                if size >= 2:
                    new_block = left_most_blocks[size - 1]
                    for i in range(size - 1):
                        if new_block.y == left_most_blocks[i].y:
                            if new_block.x < left_most_blocks[i].x:
                                left_most_blocks.remove(left_most_blocks[i])
                            elif new_block.x > left_most_blocks[i].x:
                                left_most_blocks.remove(new_block)

            for b2 in left_most_blocks:
                if b2.x - 1 < 0 or self.game.map_placed_blocks[b2.y][b2.x - 1] != 0:
                    self.can_move = False
                    break

            if self.can_move:
                for b3 in self.blocks:
                    b3.x -= 1

                self.game.update_map()
                self.game.current_shadow_shape.update_blocks(self)
                self.check_if_placed()

    def move_right(self):
        if self.game.current_shape is not None:
            self.can_move = True
            right_most_blocks = []

            for b in self.blocks:
                right_most_blocks.append(b)
                size = len(right_most_blocks)
                if size >= 2:
                    new_block = right_most_blocks[size - 1]
                    for i in range(size - 1):
                        if new_block.y == right_most_blocks[i].y:
                            if new_block.x > right_most_blocks[i].x:
                                right_most_blocks.remove(right_most_blocks[i])
                            elif new_block.x < right_most_blocks[i].x:
                                right_most_blocks.remove(new_block)

            for b2 in right_most_blocks:
                if b2.x + 1 >= c.map_size_x or self.game.map_placed_blocks[b2.y][b2.x + 1] != 0:
                    self.can_move = False
                    break

            if self.can_move:
                for b3 in self.blocks:
                    b3.x += 1

                self.game.update_map()
                self.game.current_shadow_shape.update_blocks(self)
                self.check_if_placed()

    def move_down(self):
        if self.game.current_shape is not None:
            self.can_move = True
            for b in self.blocks:
                if b.y + 1 > c.map_size_y:
                    self.can_move = False

            if self.can_move:
                for b in self.blocks:
                    b.y += 1

            self.game.update_map()
            self.game.current_shadow_shape.update_blocks(self)
            self.check_if_placed()

    def check_if_row_is_completed(self, y):
        for x in range(c.map_size_x):
            if self.game.map_placed_blocks[y][x] == 0:
                return False

        return True

    def count_completed_rows(self):
        completed_rows = 0
        for y in range(c.map_size_y - 1, 1, -1):
            if self.check_if_row_is_completed(y):
                completed_rows += 1

        return completed_rows

    def calculate_score(self, num_of_completed_rows):
        if num_of_completed_rows == 0:
            return 0
        elif num_of_completed_rows == 1:
            return 40
        elif num_of_completed_rows == 2:
            return 100
        elif num_of_completed_rows == 3:
            return 300
        elif num_of_completed_rows == 4:
            return 1200
        elif num_of_completed_rows == 5:
            return 6000

        return 0

    def score(self):
        completed_rows = self.count_completed_rows()
        self.game.score += self.calculate_score(completed_rows)
        y = c.map_size_y - 1

        while y > 1 and completed_rows != 0:
            if self.check_if_row_is_completed(y):
                for y2 in range(y, 1, -1):
                    for x in range(c.map_size_x):
                        self.game.map_placed_blocks[y2][x] = self.game.map_placed_blocks[y2 - 1][x]
                    completed_rows -= 1
                self.game.update_map()
            else:
                y -= 1

    def get_down_most_block(self):
        down_most_blocks = []
        for b in self.blocks:
            down_most_blocks.append(b)
            size = len(down_most_blocks)
            if size >= 2:
                new_block = down_most_blocks[size - 1]
                for i in range(size - 1):
                    if new_block.x == down_most_blocks[i].x:
                        if new_block.y > down_most_blocks[i].y:
                            down_most_blocks.remove(down_most_blocks[i])
                        elif new_block.y < down_most_blocks[i].y:
                            down_most_blocks.remove(new_block)

        return down_most_blocks

    def check_if_placed(self):
        down_most_blocks = self.get_down_most_block()

        # detecting placement of a block
        was_block_placed = False
        for b in down_most_blocks:
            if b.y >= c.map_size_y - 1 or self.game.map_placed_blocks[b.y + 1][b.x] != 0:
                was_block_placed = True
                break

        if was_block_placed:
            self.place_block()

    def place_block(self):
        for b in self.blocks:
            self.game.map_placed_blocks[b.y][b.x] = self.id

        self.game.update_map()
        self.score()
        self.game.current_shape = None
        self.game.current_shadow_shape = None

    def rotate(self):
        pivot = copy.deepcopy(self.blocks[self.rotational_block])
        self.is_rotation_possible = True
        next_rotation = None
        next_rotation_value = None
        next_pivot = copy.deepcopy(pivot)

        if self.rotation == len(self.states) - 1:
            next_rotation = self.states[c.ROTATIONS.state_1.value]
            next_rotation_value = c.ROTATIONS.state_1.value

            new_pivot_x = pivot.x + self.states[c.ROTATIONS.state_1.value][self.rotational_block][0]
            new_pivot_y = pivot.y + self.states[c.ROTATIONS.state_1.value][self.rotational_block][1]

            if new_pivot_x >= c.map_size_x or new_pivot_x < 0 \
                    or new_pivot_y >= c.map_size_y or new_pivot_y < 0 \
                    or self.game.map_placed_blocks[new_pivot_y][new_pivot_x] != 0:
                self.is_rotation_possible = False
            else:
                next_pivot.x += self.states[c.ROTATIONS.state_1.value][self.rotational_block][0]
                next_pivot.y += self.states[c.ROTATIONS.state_1.value][self.rotational_block][1]
        else:
            next_rotation = self.states[self.rotation + 1]
            next_rotation_value = self.rotation + 1

            new_pivot_x = pivot.x + self.states[self.rotation + 1][self.rotational_block][0]
            new_pivot_y = pivot.y + self.states[self.rotation + 1][self.rotational_block][1]

            if new_pivot_x >= c.map_size_x or new_pivot_x < 0 \
                    or new_pivot_y >= c.map_size_y or new_pivot_y < 0 \
                    or self.game.map_placed_blocks[new_pivot_y][new_pivot_x] != 0:
                self.is_rotation_possible = False
            else:
                next_pivot.x += self.states[self.rotation + 1][self.rotational_block][0]
                next_pivot.y += self.states[self.rotation + 1][self.rotational_block][1]

        if self.is_rotation_possible:
            for i in range(len(self.blocks)):  # checking if rotation is possible
                if i != self.rotational_block:
                    new_x = next_pivot.x + next_rotation[i][0]
                    new_y = next_pivot.y + next_rotation[i][1]
                else:
                    new_x = next_pivot.x
                    new_y = next_pivot.y
                if new_x >= c.map_size_x or new_x < 0 \
                        or new_y >= c.map_size_y or new_y < 0 \
                        or self.game.map_placed_blocks[new_y][new_x] != 0:
                    self.is_rotation_possible = False
                    break

        if self.is_rotation_possible:  # changing rotation
            for i in range(len(self.blocks)):
                if i != self.rotational_block:
                    self.blocks[i].x = next_pivot.x + next_rotation[i][0]
                    self.blocks[i].y = next_pivot.y + next_rotation[i][1]
                else:
                    self.blocks[i].x = next_pivot.x
                    self.blocks[i].y = next_pivot.y

            self.rotation = next_rotation_value
            self.game.update_map()
            if self.game.current_shadow_shape is not None:
                self.game.current_shadow_shape.update_blocks(self)
            self.check_if_placed()
