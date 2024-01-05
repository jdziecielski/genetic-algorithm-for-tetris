import pygame
from enum import Enum


pygame.font.init()
pygame.display.init()

class PARAMETERS(Enum):
    highest_peak_mod = 0
    agg_height_mod = 1
    bumpiness_mod = 2
    deepest_well_mod = 3
    pits_mod = 4
    holes_mod = 5
    cols_with_holes_mod = 6
    completed_rows_mod = 7
    row_transitions = 8
    col_transitions = 9


class GAME_MODE(Enum):
    TETRIS = 0
    PETRIS = 1
    TETRIS_GENETIC = 2
    PETRIS_GENETIC = 3


class ROTATIONS(Enum):
    state_1 = 0
    state_2 = 1
    state_3 = 2
    state_4 = 3
    state_5 = 4
    state_6 = 5
    state_7 = 6
    state_8 = 7

class MENU_STEPS(Enum):
    choose_game = 0
    choose_mode = 1
    game_paused = 2

class BLOCK_COLOR_TETROMINOS(Enum):
    shadow = -1
    AIR = 0
    I = 1
    O = 2
    T = 3
    S = 4
    Z = 5
    J = 6
    L = 7


class BLOCK_COLOR_PENTOMINOS(Enum):
    shadow = -1
    AIR = 0
    F = 1
    I = 2
    L = 3
    N = 4
    P = 5
    T = 6
    U = 7
    V = 8
    W = 9
    X = 10
    Y = 11
    Z = 12



SCREEN_MAX_X = 1400
SCREEN_MAX_Y = 820
text_offset = SCREEN_MAX_Y / 20

fps_cap = 120
font_size = 2
font_size_time_score = 4
window_title = "Tetris"

# game parameters
game_mode = GAME_MODE.TETRIS.value
game_mode_option = None
map_size_x = None
map_size_y = None
block_pixel_size_multiplier = 4
games_in_x = 1
games_in_y = 1
fast_game_speed = 1000
slow_game_speed = 500
game_speed = 500
num_of_tetrominos = 7
num_of_pentominos = 12


# menu parameters
is_game_paused = False
menu_step = MENU_STEPS.choose_game.value
is_menu = True
menu_steps_choose_game = 5-1
menu_steps_choose_mode = 3-1
menu_steps_paused_game = 3-1
cursor_y_diff = 0
cursor_position = 0
cursor_y = SCREEN_MAX_Y / 3
max_cursor_steps_in_current_menu = menu_steps_choose_game


# COLORS
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SCORE_COLOR = (255, 255, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
WHITE_GRID = (255, 255, 255, 100)
RED_TRANSPARENT = (255, 0, 0, 150)
GREEN_TRANSPARENT = (0, 255, 0, 100)
GREY = (219, 219, 219, 86)
SCORE_BAR_COLOR = (107, 86, 156, 61)

block_starting_point = None
block_offset = None


font = pygame.font.SysFont('verdana', font_size * 9)
font_tetris = pygame.font.SysFont('verdana', font_size * 12, True)
font_generation = pygame.font.SysFont('verdana', font_size * 8)
font_time_score = pygame.font.SysFont('myfont.ttf', font_size_time_score * 15)
font_score = pygame.font.SysFont('myfont.ttf', font_size_time_score * 15)
font_game_over = pygame.font.SysFont('verdana', font_size_time_score * 10)


screen_single_game_width = None
screen_single_game_height = None
screen_games_section_max_x = None
screen_menu_section_max_x = None


placeholders_x = None
placeholders_y = None 
screen_grid_leftover_x = None
screen_grid_leftover_y = None

screen_game_offset_x = None
screen_game_offset_y = None


menu_surface = None
game_border = None
game_grid_x = None
game_grid_y = None
best_game_surface = None
game_over_surface = None

blue_square = pygame.image.load('Graphics/Blue_square.png')
red_square = pygame.image.load('Graphics/Red_square.png')
yellow_square = pygame.image.load('Graphics/Yellow_square.png')
green_square = pygame.image.load('Graphics/Green_square.png')
pink_square = pygame.image.load('Graphics/Pink_square.png')
purple_square = pygame.image.load('Graphics/Purple_square.png')
orange_square = pygame.image.load('Graphics/Orange_square.png')
turquoise_square = pygame.image.load('Graphics/Turquoise_square.png')
grey_square = pygame.image.load('Graphics/Grey_square.png')
darkred_square = pygame.image.load('Graphics/Darkred_square.png')
brown_square = pygame.image.load('Graphics/Brown_square.png')
mint_square = pygame.image.load('Graphics/Mint_square.png')
white_square = pygame.image.load('Graphics/White_square.png').convert(32, pygame.SRCALPHA)
white_square.fill((255, 50, 255, 0))
black_square = pygame.image.load('Graphics/Black_square.png')
logo = pygame.image.load('Graphics/logo.jpg')



# tetrominoes next view
shape_tetromino_I = [[0,0,0,0,0],
                     [0,0,1,0,0],
                     [0,0,1,0,0],
                     [0,0,1,0,0],
                     [0,0,1,0,0]]

shape_tetromino_J = [[0,0,0,0,0],
                     [0,0,6,0,0],
                     [0,0,6,0,0],
                     [0,6,6,0,0],
                     [0,0,0,0,0]]

shape_tetromino_L = [[0,0,0,0,0],
                     [0,0,7,0,0],
                     [0,0,7,0,0],
                     [0,0,7,7,0],
                     [0,0,0,0,0]]

shape_tetromino_O = [[0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,2,2,0,0],
                     [0,2,2,0,0],
                     [0,0,0,0,0]]

shape_tetromino_S = [[0,0,0,0,0],
                     [0,0,4,4,0],
                     [0,4,4,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0]]

shape_tetromino_T = [[0,0,0,0,0],
                     [0,3,3,3,0],
                     [0,0,3,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0]]

shape_tetromino_Z = [[0,0,0,0,0],
                     [0,5,5,0,0],
                     [0,0,5,5,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0]]


# pentominoes next view
shape_pentomino_F = [[0,0,0,0,0],
                     [0,0,1,0,0],
                     [0,1,1,1,0],
                     [0,0,0,1,0],
                     [0,0,0,0,0]]

shape_pentomino_I = [[0,0,2,0,0],
                     [0,0,2,0,0],
                     [0,0,2,0,0],
                     [0,0,2,0,0],
                     [0,0,2,0,0]]

shape_pentomino_L = [[0,0,3,0,0],
                     [0,0,3,0,0],
                     [0,0,3,0,0],
                     [0,0,3,3,0],
                     [0,0,0,0,0]]

shape_pentomino_N = [[0,0,0,4,0],
                     [0,0,0,4,0],
                     [0,0,4,4,0],
                     [0,0,4,0,0],
                     [0,0,0,0,0]]

shape_pentomino_P = [[0,0,0,0,0],
                     [0,0,5,5,0],
                     [0,5,5,5,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0]]

shape_pentomino_T = [[0,0,0,0,0],
                     [0,6,6,6,0],
                     [0,0,6,0,0],
                     [0,0,6,0,0],
                     [0,0,0,0,0]]

shape_pentomino_U = [[0,0,0,0,0],
                     [0,7,7,7,0],
                     [0,7,0,7,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0]]

shape_pentomino_V = [[0,0,0,0,0],
                     [0,8,0,0,0],
                     [0,8,0,0,0],
                     [0,8,8,8,0],
                     [0,0,0,0,0]]

shape_pentomino_W = [[0,0,0,0,0],
                     [0,9,0,0,0],
                     [0,9,9,0,0],
                     [0,0,9,9,0],
                     [0,0,0,0,0]]

shape_pentomino_X = [[0,0,0,0,0],
                     [0,0,10,0,0],
                     [0,10,10,10,0],
                     [0,0,10,0,0],
                     [0,0,0,0,0]]

shape_pentomino_Y = [[0,0,0,0,0],
                     [0,0,11,0,0],
                     [0,0,11,0,0],
                     [0,0,11,11,0],
                     [0,0,11,0,0]]

shape_pentomino_Z = [[0,0,0,0,0],
                     [0,0,12,12,0],
                     [0,0,12,0,0],
                     [0,12,12,0,0],
                     [0,0,0,0,0]]
