import numpy as np
import pygame

pygame.init()

import constants as c
import game as g
import time
import genetic_algorithm as gA


screen = pygame.display.set_mode((c.SCREEN_MAX_X, c.SCREEN_MAX_Y))
pygame.display.set_icon(c.logo)
pygame.display.set_caption(c.window_title)
screen.fill(c.GREY)


games_list = []
next_shape_view = [[0,0,0,0,0],
                   [0,0,0,0,0],
                   [0,0,0,0,0],
                   [0,0,0,0,0],
                   [0,0,0,0,0]]

# genetic algorithm parameters
program_start_time = 0
are_games_finished = False
generation = 1
overall_high_score = 0
best_game = None
score_sum = None
games_to_go = 2

def draw_text(x, y, text):
    text = c.font.render(text, True, c.BLACK)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)

def randomise_parameters():
    return [np.random.random() * 2 - 1 for _ in range(10)]

def check_if_games_are_finished(games):
    for g in games:
        if not g.is_game_over:
            return False

    return True


def restart_games(game_list):
    for g in game_list:
        g.restart_game()


def count_remaining_agents(games):
    count = 0
    for g in games:
        if g.is_game_over is False:
            count += 1

    return count


def reset_winning_game_status(games):
    for g in games:
        g.is_game_best = False


def get_current_high_score(games):
    current_high_score = 0
    for g in games:
        if g.score > current_high_score:
            reset_winning_game_status(games)
            current_high_score = g.score
            g.is_game_best = True

    return current_high_score


def update_next_shape_view(next_shape):
    next_shape_view = None

    if c.game_mode == c.GAME_MODE.TETRIS.value:
        if next_shape == "I":
            next_shape_view = c.shape_tetromino_I
        elif next_shape == "J":
            next_shape_view = c.shape_tetromino_J
        elif next_shape == "L":
            next_shape_view = c.shape_tetromino_L
        elif next_shape == "O":
            next_shape_view = c.shape_tetromino_O
        elif next_shape == "S":
            next_shape_view = c.shape_tetromino_S
        elif next_shape == "T":
            next_shape_view = c.shape_tetromino_T
        elif next_shape == "Z":
            next_shape_view = c.shape_tetromino_Z

    elif c.game_mode == c.GAME_MODE.PETRIS.value:
        if next_shape == "I":
            next_shape_view = c.shape_pentomino_I
        elif next_shape == "F":
            next_shape_view = c.shape_pentomino_F
        elif next_shape == "L":
            next_shape_view = c.shape_pentomino_L
        elif next_shape == "N":
            next_shape_view = c.shape_pentomino_N
        elif next_shape == "P":
            next_shape_view = c.shape_pentomino_P
        elif next_shape == "T":
            next_shape_view = c.shape_pentomino_T
        elif next_shape == "U":
            next_shape_view = c.shape_pentomino_U
        elif next_shape == "V":
            next_shape_view = c.shape_pentomino_V
        elif next_shape == "W":
            next_shape_view = c.shape_pentomino_W
        elif next_shape == "X":
            next_shape_view = c.shape_pentomino_X
        elif next_shape == "Y":
            next_shape_view = c.shape_pentomino_Y
        elif next_shape == "Z":
            next_shape_view = c.shape_pentomino_Z
            
    return next_shape_view


def draw_info(gen, overall_high_score):
    screen.blit(c.menu_surface, (c.SCREEN_MAX_X - c.screen_menu_section_max_x, 0))

    title = ""
    if c.game_mode is c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value:
        title = "Tetris"
    else:
        title = "Petris"

    draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.text_offset, title)
    draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset, "Esc - Exit")
    draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset*2 , "P - Pause Game")

    if c.game_mode is c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value:
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.text_offset * 3, "Generation #" + str(gen))
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x / 2, c.text_offset * 4, "Remaining Agents: " + str(count_remaining_agents(games_list)) + "/" + str(c.games_in_x * c.games_in_y))
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x / 2, c.text_offset * 5, "Current High Score: " + str(get_current_high_score(games_list)))
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x / 2, c.text_offset* 6, "Overall High Score: " + str(overall_high_score))
    elif c.game_mode is c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.PETRIS.value:
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset * 10, "Controls:")
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset * 9, "Up Arrow - Rotate Shape")
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset * 8, "Left Arrow - Move Left")
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset * 7, "Right Arrow - Move Right")
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset * 6, "Down Arrow - Move Down")
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset * 5, "Space - Drop Shape") 
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x/2, c.SCREEN_MAX_Y - c.text_offset * 3, "R - Restart Game")

    

def draw_next_shape_view():
    if c.game_mode is c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.PETRIS.value:
        next_shape_view = update_next_shape_view(game.next_shape)
        draw_text(c.SCREEN_MAX_X - c.screen_menu_section_max_x / 2,  c.text_offset*4, "Next shape:")

        if next_shape_view is not None:
            if c.game_mode == c.GAME_MODE.TETRIS.value:
                for y in range(len(next_shape_view)):
                    for x in range (len(next_shape_view[y])):
                        if next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.AIR.value:
                            screen.blit(c.black_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.shadow.value:
                            screen.blit(c.white_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.I.value:
                            screen.blit(c.blue_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.O.value:
                            screen.blit(c.red_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.T.value:
                            screen.blit(c.green_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.S.value:
                            screen.blit(c.orange_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.Z.value:
                            screen.blit(c.pink_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.J.value:
                            screen.blit(c.purple_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_TETROMINOS.L.value:
                            screen.blit(c.yellow_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                            y * c.block_offset +c.text_offset*5))
            elif c.game_mode == c.GAME_MODE.PETRIS.value:
                for y in range(len(next_shape_view)):
                    for x in range (len(next_shape_view[y])):
                        if next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.AIR.value:
                            screen.blit(c.black_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.shadow.value:
                            screen.blit(c.white_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.F.value:
                            screen.blit(c.blue_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.I.value:
                            screen.blit(c.red_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.L.value:
                            screen.blit(c.green_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.N.value:
                            screen.blit(c.orange_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.P.value:
                            screen.blit(c.pink_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.T.value:
                            screen.blit(c.purple_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.U.value:
                            screen.blit(c.yellow_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.V.value:
                            screen.blit(c.turquoise_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.W.value:
                            screen.blit(c.mint_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.X.value:
                            screen.blit(c.grey_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.Y.value:
                         screen.blit(c.darkred_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
                        elif next_shape_view[y][x] == c.BLOCK_COLOR_PENTOMINOS.Z.value:
                            screen.blit(c.brown_square, ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2),
                                                                y * c.block_offset +c.text_offset*5))
            
            for y in range(1, 6):
                screen.blit(c.game_grid_x, (c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2), 
                                            y * c.block_offset + c.text_offset*5))

            for x in range(5):
                screen.blit(c.game_grid_y,
                                ((x * c.block_offset) + c.SCREEN_MAX_X - c.screen_menu_section_max_x + (c.block_offset*3 / 2), c.text_offset*5))


def draw_menu():
    screen.fill(c.GREY)
    
    draw_text(c.SCREEN_MAX_X/3, c.cursor_y + c.text_offset + c.cursor_y_diff, ">")
    
    if c.menu_step == c.MENU_STEPS.choose_game.value:
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3, "Choose Game Option...")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset, "Tetris")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*2, "Petris")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*3, "Tetris + Genetic Algorithm")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*4, "Petris + Genetic Algorithm")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*5, "Exit")

    elif c.menu_step == c.MENU_STEPS.choose_mode.value:
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3, "Choose Game Option...")

        text = None
        if c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.PETRIS.value: text = "1 - Slow Speed"
        elif c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value: text = "1 - 72 instances"
        elif c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value: text = "1 - 36 instances"

        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset, text)

        text = None
        if c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.PETRIS.value: text = "2 - Fast Speed"
        elif c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value: text = "2 - 15 instances"
        elif c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value: text = "2 - 8 instances"
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*2, text)

        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*3, "Back")

    elif c.menu_step == c.MENU_STEPS.game_paused.value:
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3, "Game is Paused...")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset, "Resume")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*2, "Go to Main Menu")
        draw_text(c.SCREEN_MAX_X/2, c.SCREEN_MAX_Y / 3 + c.text_offset*3, "Exit")


def menu_event_listener(events):
    global games_list

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                unpause_game()
                
            if event.key == pygame.K_DOWN:
                c.cursor_position += 1

                if c.cursor_position > c.max_cursor_steps_in_current_menu: 
                    c.cursor_position = 0
                    c.cursor_y_diff = 0
                else: 
                    c.cursor_y_diff += c.text_offset
                
            elif event.key == pygame.K_UP:
                c.cursor_position -= 1

                if c.cursor_position < 0:
                    c.cursor_position = c.max_cursor_steps_in_current_menu
                    c.cursor_y_diff = c.text_offset * c.max_cursor_steps_in_current_menu
                else:
                    c.cursor_y_diff -= c.text_offset
            

            elif event.key == pygame.K_RETURN:                                  # enter
                if c.menu_step == c.MENU_STEPS.choose_mode.value:
                    if c.cursor_position == c.menu_steps_choose_mode:         # back button
                        c.cursor_y_diff = 0
                        c.cursor_position = 0
                        c.max_cursor_steps_in_current_menu = c.menu_steps_choose_game
                        c.menu_step = c.MENU_STEPS.choose_game.value
                    else:                                                   # choose game mode
                        c.game_mode_option = c.cursor_position + 1
                        c.is_menu = False
                        c.menu_step = c.MENU_STEPS.choose_game.value
                        c.max_cursor_steps_in_current_menu = c.menu_steps_choose_game
                        init_games()

                elif c.menu_step == c.MENU_STEPS.choose_game.value:           # choose game
                    if c.cursor_position == c.menu_steps_choose_game: pygame.quit()
                    else:    
                        c.game_mode = c.cursor_position
                        c.max_cursor_steps_in_current_menu = c.menu_steps_choose_mode
                        c.cursor_y_diff = 0
                        c.menu_step = c.MENU_STEPS.choose_mode.value
                        c.cursor_position = 0
                
                elif c.menu_step == c.MENU_STEPS.game_paused.value:         # paused game menu
                    if c.cursor_position == 0: unpause_game()               # resume game
                    elif c.cursor_position == 1:                            # go back to main menu
                        c.cursor_y_diff = 0
                        c.cursor_position = 0
                        c.max_cursor_steps_in_current_menu = c.menu_steps_choose_game
                        c.menu_step = c.MENU_STEPS.choose_game.value
                        clear_games()
                    elif c.cursor_position == 2: pygame.quit()              # exit game


                screen.fill(c.GREY)
            
        elif event.type == pygame.QUIT:
            pygame.quit()


def add_scores(games_list, score_sum):
    for i in range(len(games_list)):
        score_sum[i] += games_list[i].score


def load_textures():
    c.blue_square = pygame.image.load('Graphics/Blue_square.png')
    c.red_square = pygame.image.load('Graphics/Red_square.png')
    c.yellow_square = pygame.image.load('Graphics/Yellow_square.png')
    c.green_square = pygame.image.load('Graphics/Green_square.png')
    c.pink_square = pygame.image.load('Graphics/Pink_square.png')
    c.purple_square = pygame.image.load('Graphics/Purple_square.png')
    c.orange_square = pygame.image.load('Graphics/Orange_square.png')
    c.turquoise_square = pygame.image.load('Graphics/Turquoise_square.png')
    c.grey_square = pygame.image.load('Graphics/Grey_square.png')
    c.darkred_square = pygame.image.load('Graphics/Darkred_square.png')
    c.brown_square = pygame.image.load('Graphics/Brown_square.png')
    c.mint_square = pygame.image.load('Graphics/Mint_square.png')
    c.white_square = pygame.image.load('Graphics/White_square.png').convert(32, pygame.SRCALPHA)
    c.white_square.fill((255, 50, 255, 0))
    c.black_square = pygame.image.load('Graphics/Black_square.png')
    c.logo = pygame.image.load('Graphics/logo.jpg')


def genetic_algorithm(games_list):
    global generation, score_sum, games_to_go, overall_high_score

    if c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value:
        if check_if_games_are_finished(games_list):
            add_scores(games_list, score_sum)
            high_score = get_current_high_score(games_list)

            if high_score > overall_high_score: overall_high_score = high_score
            
            if games_to_go == 0:
                for i in range(len(games_list)):
                    games_list[i].score = score_sum[i]
                    score_sum[i] = 0

                games_list = gA.elitify_and_crossover(games_list)
                games_list = gA.mutate(games_list)
                generation += 1
                games_to_go = 3
            
            restart_games(games_list)
            games_to_go -= 1

def clear_games():
    global games_list, games_to_go, next_shape_view, program_start_time, overall_high_score

    next_shape_view =   [[0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]]

    games_list.clear()

    overall_high_score = 0
    games_to_go = 2
    program_start_time = 0
    c.games_in_x = 1
    c.games_in_y = 1
    c.game_speed = 500
    c.block_pixel_size_multiplier = 4
    c.font_size_time_score = 4
    c.map_size_x = None
    c.map_size_y = None
    c.game_mode_option = None
    c.block_starting_point = None
    c.block_offset = None
    c.screen_single_game_width = None
    c.screen_single_game_height = None
    c.screen_games_section_max_x = None
    c.screen_menu_section_max_x = None
    c.screen_grid_leftover_x = None
    c.placeholders_x = None
    c.placeholders_y = None
    c.screen_grid_leftover_y = None
    c.screen_game_offset_x = None
    c.screen_game_offset_y = None
    c.menu_surface = None
    c.game_border = None
    c.game_grid_x = None
    c.game_grid_y = None
    c.best_game_surface = None
    c.game_over_surface = None
    c.font_time_score = None
    c.font_score = None
    c.blue_square = None
    c.red_square = None
    c.yellow_square = None
    c.green_square = None
    c.pink_square = None
    c.purple_square = None 
    c.orange_square = None
    c.turquoise_square = None
    c.grey_square = None
    c.darkred_square = None
    c.brown_square = None
    c.mint_square = None
    c.white_square = None
    c.black_square = None
            
def init_games():
    global games_list, best_game, score_sum, program_start_time

    load_textures()

    if c.game_mode is c.GAME_MODE.PETRIS_GENETIC.value or c.game_mode is c.GAME_MODE.PETRIS.value:
        c.map_size_x = 15
        c.map_size_y = 25
    else:
        c.map_size_x = 10
        c.map_size_y = 16

    if c.game_mode == c.GAME_MODE.TETRIS.value or c.game_mode == c.GAME_MODE.PETRIS.value:
        if c.game_mode_option == 1:
            c.game_speed = c.fast_game_speed
        elif c.game_mode_option == 2:
            c.game_speed = c.slow_game_speed    
    
    elif c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value:
        if c.game_mode_option == 1:
            c.games_in_x = 12
            c.games_in_y = 6
            c.block_pixel_size_multiplier = 1
            c.font_size_time_score = 1
        elif c.game_mode_option == 2:
            c.games_in_x = 5
            c.games_in_y = 3
            c.block_pixel_size_multiplier = 2
            c.font_size_time_score = 2
    
    elif c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value:
        if c.game_mode_option == 1:
            c.games_in_x = 9
            c.games_in_y = 4
            c.block_pixel_size_multiplier = 1
            c.font_size_time_score = 1
        elif c.game_mode_option == 2:
            c.games_in_x = 4
            c.games_in_y = 2
            c.block_pixel_size_multiplier = 2
            c.font_size_time_score = 2

    c.block_starting_point = [c.map_size_x // 2, 1]
    c.block_offset = c.block_pixel_size_multiplier * 8  # don't change!
    c.screen_single_game_width = c.block_offset * c.map_size_x
    c.screen_single_game_height = (c.block_offset) * c.map_size_y
    c.screen_games_section_max_x = c.SCREEN_MAX_X * 0.8
    c.screen_menu_section_max_x = c.SCREEN_MAX_X - c.screen_games_section_max_x

    if c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value:
        c.placeholders_x = c.games_in_x - 1  
    else: 
        c.placeholders_x = 1 

    if c.game_mode == c.GAME_MODE.TETRIS_GENETIC.value or c.game_mode == c.GAME_MODE.PETRIS_GENETIC.value:
        c.placeholders_y = c.games_in_y - 1
    else:
        c.placeholders_y = 1
         
    c.screen_grid_leftover_x = c.screen_games_section_max_x - (c.screen_single_game_width * c.games_in_x)
    c.screen_grid_leftover_y = c.SCREEN_MAX_Y - (c.screen_single_game_height * c.games_in_y)
    c.screen_game_offset_x = c.screen_grid_leftover_x / (c.placeholders_x)
    c.screen_game_offset_y = c.screen_grid_leftover_y / (c.placeholders_y)

    c.menu_surface = pygame.Surface((c.screen_menu_section_max_x, c.SCREEN_MAX_Y))
    c.menu_surface.fill(c.WHITE_GRID)

    c.game_border = pygame.Surface((c.screen_single_game_width, c.block_offset))
    c.game_border.fill(c.SCORE_BAR_COLOR)

    c.game_grid_x = pygame.Surface((c.screen_single_game_width, 1), pygame.SRCALPHA, 32)
    c.game_grid_x.fill(c.WHITE_GRID)

    c.game_grid_y = pygame.Surface((1, c.screen_single_game_height - c.block_offset), pygame.SRCALPHA, 32)
    c.game_grid_y.fill(c.WHITE_GRID)

    c.best_game_surface = pygame.Surface((c.screen_single_game_width, c.screen_single_game_height), pygame.SRCALPHA, 32)
    c.best_game_surface.fill(c.GREEN_TRANSPARENT)

    c.game_over_surface = pygame.Surface((c.screen_single_game_width, c.screen_single_game_height), pygame.SRCALPHA, 32)
    c.game_over_surface.fill(c.RED_TRANSPARENT)

    c.font_time_score = pygame.font.SysFont('myfont.ttf', c.font_size_time_score * 15)
    c.font_score = pygame.font.SysFont('myfont.ttf', c.font_size_time_score * 15)

    for y in range(c.games_in_y):
        for x in range(c.games_in_x):
            game = g.Game(screen, x, y, games_list, randomise_parameters())
            games_list.append(game)
    
    best_game = games_list[0]
    score_sum = [0 for _ in range(c.games_in_y * c.games_in_x)]

    c.blue_square = pygame.transform.scale_by(c.blue_square, c.block_pixel_size_multiplier)
    c.red_square = pygame.transform.scale_by(c.red_square, c.block_pixel_size_multiplier)
    c.yellow_square = pygame.transform.scale_by(c.yellow_square, c.block_pixel_size_multiplier)
    c.green_square = pygame.transform.scale_by(c.green_square, c.block_pixel_size_multiplier)
    c.pink_square = pygame.transform.scale_by(c.pink_square, c.block_pixel_size_multiplier)
    c.purple_square = pygame.transform.scale_by(c.purple_square, c.block_pixel_size_multiplier)
    c.orange_square = pygame.transform.scale_by(c.orange_square, c.block_pixel_size_multiplier)
    c.turquoise_square = pygame.transform.scale_by(c.turquoise_square, c.block_pixel_size_multiplier)
    c.grey_square = pygame.transform.scale_by(c.grey_square, c.block_pixel_size_multiplier)
    c.darkred_square = pygame.transform.scale_by(c.darkred_square, c.block_pixel_size_multiplier)
    c.brown_square = pygame.transform.scale_by(c.brown_square, c.block_pixel_size_multiplier)
    c.mint_square = pygame.transform.scale_by(c.mint_square, c.block_pixel_size_multiplier)
    c.white_square = pygame.transform.scale_by(c.white_square, c.block_pixel_size_multiplier)
    c.black_square = pygame.transform.scale_by(c.black_square, c.block_pixel_size_multiplier)
    
    c.is_game_paused = False
    program_start_time = time.process_time()



def unpause_game():
    if c.is_game_paused == True:
        c.is_game_paused = False
        c.menu_step = c.MENU_STEPS.choose_game.value
        c.is_menu = False
        c.max_cursor_steps_in_current_menu = c.menu_steps_choose_game
        c.cursor_position = 0
        screen.fill(c.GREY)

while True:
    if c.is_menu:
        draw_menu()
        events = pygame.event.get()
        menu_event_listener(events)

    if not c.is_menu:
        if not c.is_game_paused and games_list != None:
            for game in games_list:
                if game != None:
                    game.game()
                        
                    if game.score > best_game.score:
                        best_game = game
                
        draw_info(generation, overall_high_score)
        draw_next_shape_view()
        genetic_algorithm(games_list)

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        break

    pygame.display.flip()
pygame.quit()
