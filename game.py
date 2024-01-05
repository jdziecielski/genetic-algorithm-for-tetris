import random
import time

import pygame
import numpy as np
import copy

from Tetrominos import tetrominoI as tI
from Tetrominos import tetrominoO as tO
from Tetrominos import tetrominoT as tT
from Tetrominos import tetrominoS as tS
from Tetrominos import tetrominoZ as tZ
from Tetrominos import tetrominoJ as tJ
from Tetrominos import tetrominoL as tL

from Pentominos import pentominoF as pF
from Pentominos import pentominoI as pI
from Pentominos import pentominoL as pL
from Pentominos import pentominoN as pN
from Pentominos import pentominoP as pP
from Pentominos import pentominoT as pT
from Pentominos import pentominoU as pU
from Pentominos import pentominoV as pV
from Pentominos import pentominoW as pW
from Pentominos import pentominoX as pX
from Pentominos import pentominoY as pY
from Pentominos import pentominoZ as pZ

import shadow_mino as sM
import genetic_algorithm as g

import constants as c


def is_wall_on_the_left(game):
    for block in game.current_shape.blocks:
        if block.x == 0:
            return True

    return False


def is_wall_on_the_right(game):
    for block in game.current_shape.blocks:
        if block.x == c.map_size_x - 1:
            return True

    return False


def reset_position(game, starting_position):
    if game.current_shape is not None:
        for i in range(len(game.current_shape.blocks)):
            game.current_shape.blocks[i].x = starting_position[i].x
            game.current_shape.blocks[i].y = starting_position[i].y


def find_best_position(game):
    count = 1
    shape = game.current_shape
    map = copy.deepcopy(game.map_placed_blocks)
    placed_shape_position = game.current_shadow_shape
    starting_position = copy.deepcopy(shape.blocks)
    best_move_score = -1000
    best_move_count = 1
    best_move_position = copy.deepcopy(placed_shape_position.blocks)

    for _ in range(len(shape.states)):
        for i in range(2):
            last_move_x = None
            last_move_rotation = None
            starting_position = copy.deepcopy(shape.blocks)
            while True:

                if game.current_shape is None:
                    break

                placed_shape_position = game.current_shadow_shape

                if last_move_x == shape.blocks[shape.rotational_block].x and last_move_rotation == shape.rotation:
                    # game.if_game_ended()
                    break

                # create map with view of placed block
                for b in placed_shape_position.blocks:
                    map[b.y][b.x] = 1

                # evaluate score with fitness function
                current_move_score = g.fitness_function(game, map)

                if current_move_score > best_move_score:
                    best_move_score = current_move_score
                    best_move_position = copy.deepcopy(placed_shape_position.blocks)
                    best_move_count = count

                # save last move to break the loop if the move repeats
                last_move_rotation = shape.rotation
                last_move_x = shape.blocks[shape.rotational_block].x

                # revert changes
                for b in placed_shape_position.blocks:
                    map[b.y][b.x] = 0

                # go left
                if i == 0:
                    if is_wall_on_the_left(game) is False:
                        shape.move_left()
                    else:
                        # reset position to the middle and skip already checked position
                        reset_position(game, starting_position)
                        shape.move_right()
                        break
                # go right
                elif i == 1:
                    if is_wall_on_the_right(game) is False:
                        shape.move_right()
                    else:
                        break

        # reset position and go to the next rotation
        reset_position(game, starting_position)
        shape.rotate()

    # execute move
    game.place_block_in_position(best_move_position)


class Game:
    def __init__(self, screen, game_x_id, game_y_id, games_list, parameters):
        self.screen = screen
        self.clock = pygame.time.Clock()

        if c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value:
            self.game_window_x = c.screen_single_game_width * game_x_id + (c.screen_game_offset_x * game_x_id)
            self.game_window_y = c.screen_single_game_height * game_y_id + (c.screen_game_offset_y * game_y_id)
        else:
            self.game_window_x = c.screen_games_section_max_x/2 - (c.screen_single_game_width/2)
            self.game_window_y = c.SCREEN_MAX_Y/2 - c.screen_single_game_height/2
            
        self.map_to_draw = [[0 for _ in range(c.map_size_x)] for _ in range(c.map_size_y)]
        self.map_placed_blocks = [[0 for _ in range(c.map_size_x)] for _ in range(c.map_size_y)]
        self.game_x_id = game_x_id
        self.game_y_id = game_y_id
        self.drop_block_event = pygame.USEREVENT + 1
        self.current_shape = None
        pygame.time.set_timer(self.drop_block_event, c.game_speed)
        self.current_shadow_shape = None
        self.running = True
        self.is_game_over = False
        self.is_game_best = False
        self.score = 0
        self.games_list = games_list
        self.runtime = 0
        self.parameters = parameters
        self.parameters = [-0.8820700751642538, -0.9670434047671908, 0.1120009261169228, -0.722014751329078,
                           -0.46014572028128964, -0.2904645804865835, -0.9546435516437437, 0.595940344697798,
                           -0.6708102363724926, -0.2647385269386282]

        self.is_first_bag = True
        self.shapes_bag = None
        self.shapes_bag2 = None
        self.next_shape = None

        if c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value:
            self.shapes_bag = self.generate_tetromino_bag()
            self.shapes_bag2 = self.generate_tetromino_bag()
        else:
            self.shapes_bag = self.generate_pentomino_bag()
            self.shapes_bag2 = self.generate_pentomino_bag()

    def if_game_ended(self):
        if self.current_shape is not None:
            for block in self.current_shape.blocks:
                if self.map_placed_blocks[block.y][block.x] != 0:
                    self.is_game_over = True
                    self.is_game_best = False
                    break

    def restart_game(self):
        self.screen.fill(c.GREY)
        self.clear_map()
        self.current_shape = None
        self.score = 0
        self.runtime = 0
        self.is_game_over = False
        self.is_game_best = False
        self.is_first_bag = True
        self.shapes_bag = []

    def clear_map(self):
        for y in range(1, c.map_size_y):
            for x in range(c.map_size_x):
                self.map_to_draw[y][x] = 0
                self.map_placed_blocks[y][x] = 0

    def update_map(self):
        for y in range(c.map_size_y):
            for x in range(c.map_size_x):
                self.map_to_draw[y][x] = self.map_placed_blocks[y][x]

        if self.current_shape is not None:
            for b in self.current_shape.blocks:
                self.map_to_draw[b.y][b.x] = self.current_shape.id
        
        if c.game_mode == c.GAME_MODE.PETRIS.value or c.game_mode == c.GAME_MODE.TETRIS.value:
            if self.current_shadow_shape is not None and self.is_game_over == False:
                for b in self.current_shadow_shape.blocks:
                    if b.y < c.map_size_y and b.x < c.map_size_x:
                        self.map_to_draw[b.y][b.x] = self.current_shadow_shape.id


    def generate_tetromino_bag(self):
        bag = []
        if not self.is_first_bag:
            bag.extend(["I", "O", "T", "S", "Z", "J", "L"])
            random.shuffle(bag)
        else:
            bag = ["I", "J", "L", "T"]
            random.shuffle(bag)
            rest_of_shapes = ["O", "S", "Z"]
            random.shuffle(rest_of_shapes)
            bag += rest_of_shapes
            self.is_first_bag = False
            self.next_shape = bag[1]
        
        return bag
    
    def generate_pentomino_bag(self):
        bag = []
        if not self.is_first_bag:
            bag.extend(["F", "I", "L", "N", "P", "T", "U", "V", "W", "X", "Y", "Z"])
            random.shuffle(self.shapes_bag)
        else:
            bag = ["I", "L", "P", "T", "U", "V", "Y"]
            random.shuffle(bag)
            rest_of_shapes = ["F", "N", "W", "X", "Z"]
            random.shuffle(rest_of_shapes)
            bag += rest_of_shapes
            self.is_first_bag = False
            self.next_shape = bag[1]
        
        return bag

    def generate_tetromino_from_bag(self):
        new_shape = None

        if len(self.shapes_bag) == 0:
            self.shapes_bag = copy.deepcopy(self.shapes_bag2)
            self.shapes_bag2 = self.generate_tetromino_bag()

        if self.shapes_bag[0] == "I":
            new_shape = tI.TetrominoI(self)
        elif self.shapes_bag[0] == "J":
            new_shape = tJ.TetrominoJ(self)
        elif self.shapes_bag[0] == "T":
            new_shape = tT.TetrominoT(self)
        elif self.shapes_bag[0] == "O":
            new_shape = tO.TetrominoO(self)
        elif self.shapes_bag[0] == "S":
            new_shape = tS.TetrominoS(self)
        elif self.shapes_bag[0] == "Z":
            new_shape = tZ.TetrominoZ(self)
        elif self.shapes_bag[0] == "L":
            new_shape = tL.TetrominoL(self)

        self.shapes_bag.pop(0)
        self.current_shape = new_shape
        self.current_shadow_shape = sM.Shadowmino(self, new_shape)
        if len(self.shapes_bag) == 0:
            self.next_shape = self.shapes_bag2[0]
        else:
            self.next_shape = self.shapes_bag[0]

        self.if_game_ended()

        # genetic algorithm block placement
        if (c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value):
            find_best_position(self)


    def generate_pentomino_from_bag(self):
        new_shape = None

        if len(self.shapes_bag) == 0:
            self.shapes_bag = copy.deepcopy(self.shapes_bag2)
            self.shapes_bag2 = self.generate_pentomino_bag()

        if self.shapes_bag[0] == "F":
            new_shape = pF.PentominoF(self)
        elif self.shapes_bag[0] == "I":
            new_shape = pI.PentominoI(self)
        elif self.shapes_bag[0] == "L":
            new_shape = pL.PentominoL(self)
        elif self.shapes_bag[0] == "N":
            new_shape = pN.PentominoN(self)
        elif self.shapes_bag[0] == "P":
            new_shape = pP.PentominoP(self)
        elif self.shapes_bag[0] == "T":
            new_shape = pT.PentominoT(self)
        elif self.shapes_bag[0] == "U":
            new_shape = pU.PentominoU(self)
        elif self.shapes_bag[0] == "V":
            new_shape = pV.PentominoV(self)
        elif self.shapes_bag[0] == "W":
            new_shape = pW.PentominoW(self)
        elif self.shapes_bag[0] == "X":
            new_shape = pX.PentominoX(self)
        elif self.shapes_bag[0] == "Y":
            new_shape = pY.PentominoY(self)
        elif self.shapes_bag[0] == "Z":
            new_shape = pZ.PentominoZ(self)
        

        self.shapes_bag.pop(0)
        self.current_shape = new_shape
        self.current_shadow_shape = sM.Shadowmino(self, new_shape)
        if len(self.shapes_bag) == 0:
            self.next_shape = self.shapes_bag2[0]
        else:
            self.next_shape = self.shapes_bag[0]    
        self.if_game_ended()

        # genetic algorithm block placement
        if (c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value):
            find_best_position(self)


    def draw_info(self):
        score_text = c.font_score.render(str(self.score), True, c.SCORE_COLOR)
        score_info_rect = score_text.get_rect()
        score_info_rect.center = (
            self.game_window_x + (c.screen_single_game_width / 2), score_info_rect.height/2 + self.game_window_y)
        self.screen.blit(score_text, score_info_rect)

    def draw_time(self):
        # score_text = c.font.render('Score: ' + str(self.score), True, c.GREEN)
        runtime_text = c.font_time_score.render(str(self.runtime), True, c.BLACK)
        runtime_info_rect = runtime_text.get_rect()
        runtime_info_rect.center = (self.game_window_x + runtime_info_rect.width/2, self.game_window_y + runtime_info_rect.height/2)
        self.screen.blit(runtime_text, runtime_info_rect)

    def place_block_in_position(self, blocks):
        if self.current_shape is not None:
            for i in range(len(blocks)):
                self.current_shape.blocks[i].x = blocks[i].x
                self.current_shape.blocks[i].y = blocks[i].y

            self.current_shape.place_block()

    def draw_map_tetrominos(self):
        for y in range(c.map_size_y):
            for x in range(c.map_size_x):
                if self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.AIR.value:
                    self.screen.blit(c.black_square, (x * c.block_offset + self.game_window_x,
                                                      y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.shadow.value:
                    self.screen.blit(c.white_square, (x * c.block_offset + self.game_window_x,
                                                      y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.I.value:
                    self.screen.blit(c.blue_square, (x * c.block_offset + self.game_window_x,
                                                     y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.O.value:
                    self.screen.blit(c.red_square, (x * c.block_offset + self.game_window_x,
                                                    y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.T.value:
                    self.screen.blit(c.green_square, (x * c.block_offset + self.game_window_x,
                                                      y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.S.value:
                    self.screen.blit(c.orange_square, (x * c.block_offset + self.game_window_x,
                                                       y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.Z.value:
                    self.screen.blit(c.pink_square, (x * c.block_offset + self.game_window_x,
                                                     y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.J.value:
                    self.screen.blit(c.purple_square, (x * c.block_offset + self.game_window_x,
                                                       y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_TETROMINOS.L.value:
                    self.screen.blit(c.yellow_square, (x * c.block_offset + self.game_window_x,
                                                       y * c.block_offset + self.game_window_y))

                self.screen.blit(c.game_border, (self.game_window_x, self.game_window_y))

    def draw_map_pentominos(self):
        for y in range(c.map_size_y):
            for x in range(c.map_size_x):
                if self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.AIR.value:
                    self.screen.blit(c.black_square, (x * c.block_offset + self.game_window_x,
                                                      y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.shadow.value:
                    self.screen.blit(c.white_square, (x * c.block_offset + self.game_window_x,
                                                      y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.F.value:
                    self.screen.blit(c.blue_square, (x * c.block_offset + self.game_window_x,
                                                     y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.I.value:
                    self.screen.blit(c.red_square, (x * c.block_offset + self.game_window_x,
                                                    y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.L.value:
                    self.screen.blit(c.green_square, (x * c.block_offset + self.game_window_x,
                                                      y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.N.value:
                    self.screen.blit(c.orange_square, (x * c.block_offset + self.game_window_x,
                                                       y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.P.value:
                    self.screen.blit(c.pink_square, (x * c.block_offset + self.game_window_x,
                                                     y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.T.value:
                    self.screen.blit(c.purple_square, (x * c.block_offset + self.game_window_x,
                                                       y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.U.value:
                    self.screen.blit(c.yellow_square, (x * c.block_offset + self.game_window_x,
                                                       y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.V.value:
                    self.screen.blit(c.turquoise_square, (x * c.block_offset + self.game_window_x,
                                                          y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.W.value:
                    self.screen.blit(c.mint_square, (x * c.block_offset + self.game_window_x,
                                                     y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.X.value:
                    self.screen.blit(c.grey_square, (x * c.block_offset + self.game_window_x,
                                                     y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.Y.value:
                    self.screen.blit(c.darkred_square, (x * c.block_offset + self.game_window_x,
                                                        y * c.block_offset + self.game_window_y))
                elif self.map_to_draw[y][x] == c.BLOCK_COLOR_PENTOMINOS.Z.value:
                    self.screen.blit(c.brown_square, (x * c.block_offset + self.game_window_x,
                                                      y * c.block_offset + self.game_window_y))

        self.screen.blit(c.game_border, (self.game_window_x, self.game_window_y))

    def draw_grids(self):
        for y in range(2, c.map_size_y):
            self.screen.blit(c.game_grid_x, (self.game_window_x, y * c.block_offset + self.game_window_y))

        for x in range(c.map_size_x):
            self.screen.blit(c.game_grid_y,
                             (x * c.block_offset + self.game_window_x, self.game_window_y + c.block_offset))

    def pause_game(self):
        if c.is_game_paused == False:
            c.is_menu = True
            c.menu_step = c.MENU_STEPS.game_paused.value
            c.is_game_paused = True
            c.max_cursor_steps_in_current_menu = c.menu_steps_paused_game
            c.cursor_position = 0
            c.cursor_y_diff = 0

    def do_events(self, events):
        if self.current_shape is None and not self.is_game_over:
            if c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value:
                self.generate_tetromino_from_bag()
            else:
                self.generate_pentomino_from_bag()


        for event in events:
            # restart game
            if event.type == pygame.KEYDOWN and (c.game_mode == c.GAME_MODE.PETRIS.value or c.game_mode == c.GAME_MODE.TETRIS.value):
                if event.key == pygame.K_r: self.restart_game()
            elif event.type == pygame.QUIT: pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: self.pause_game()

            # block movement
            if c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.PETRIS.value:
                if not self.is_game_over and not c.is_game_paused:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if self.current_shape is not None:
                                self.current_shape.rotate()
                        elif event.key == pygame.K_LEFT:
                            if self.current_shape is not None:
                                self.current_shape.move_left()
                        elif event.key == pygame.K_RIGHT:
                            if self.current_shape is not None:
                                self.current_shape.move_right()
                        elif event.key == pygame.K_SPACE:
                            if self.current_shape is not None:
                                self.place_block_in_position(self.current_shadow_shape.blocks)
                        

                    if pygame.key.get_pressed()[pygame.K_DOWN]:
                        if self.current_shape is not None:
                            self.current_shape.move_down()

                    if event.type == self.drop_block_event:
                        if self.current_shape is not None:
                            self.current_shape.move_down()
                    

    def game_over(self):
        self.screen.blit(c.game_over_surface, (self.game_window_x, self.game_window_y))

        if c.game_mode is c.GAME_MODE.PETRIS.value or c.game_mode is c.GAME_MODE.TETRIS.value:
            text = c.font_game_over.render("Game Over!", True, c.BLACK)
            text_rect = text.get_rect()
            text_rect.center = (self.game_window_x + c.screen_single_game_width/2, 
                                self.game_window_y/4)
            self.screen.blit(text, text_rect)

            text = c.font_game_over.render("Press 'R' to Restart...", True, c.BLACK)
            text_rect = text.get_rect()
            text_rect.center = (self.game_window_x + c.screen_single_game_width/2, 
                                self.game_window_y/4 + text_rect.height)
            self.screen.blit(text, text_rect)


    def best_game(self):
        self.screen.blit(c.best_game_surface, (self.game_window_x, self.game_window_y))

    def game(self):
        if not self.is_game_over:
            self.update_map()

        events = pygame.event.get()
        if self.do_events(events) == False:
            self.running = False

        if c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value:
            self.draw_map_tetrominos()
        elif c.game_mode == c.GAME_MODE.PETRIS.value or c.GAME_MODE.PETRIS_GENETIC.value:
            self.draw_map_pentominos()
        
        self.draw_info()
        self.draw_grids()
        if c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value:
            self.draw_time()
        
        if self.is_game_over:
            self.game_over()
        else:
            self.runtime += 1

        # green highlight for best game
        if self.is_game_best and (c.game_mode is c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode is c.GAME_MODE.PETRIS_GENETIC.value):
            self.best_game()

        pygame.display.flip()
        self.clock.tick(c.fps_cap)