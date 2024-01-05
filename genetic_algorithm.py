import constants as c
import numpy as np
import copy


def calculate_peaks(map):
    peaks = [0 for _ in range(c.map_size_x)]
    for x in range(c.map_size_x):
        for y in range(c.map_size_y):
            if map[y][x] != 0:
                peaks[x] = np.abs(c.map_size_y - y)
                break

    return peaks


def calculate_aggregate_height(peaks): return np.sum(peaks)


def calculate_bumpiness(peaks):
    bumpiness = 0
    for i in range(c.map_size_x - 1):
        bumpiness += np.abs(peaks[i] - peaks[i + 1])
    return bumpiness


def calculate_wells(peaks):
    wells = []
    for i in range(len(peaks)):
        if i == 0:
            well = peaks[1] - peaks[0]
            well = well if well > 0 else 0
            wells.append(well)
        elif i == len(peaks) - 1:
            well = peaks[-2] - peaks[-1]
            well = well if well > 0 else 0
            wells.append(well)
        else:
            well1 = peaks[i - 1] - peaks[i]
            well2 = peaks[i + 1] - peaks[i]
            well1 = well1 if well1 > 0 else 0
            well2 = well2 if well2 > 0 else 0
            well = well1 if well1 >= well2 else well2
            wells.append(well)
    return wells


def calculate_pits(peaks):
    num_of_pits = 0
    for p in peaks:
        if p == 0:
            num_of_pits += 1

    return num_of_pits


def calculate_holes(peaks, map):
    holes = [0 for _ in range(c.map_size_x)]
    for x in range(c.map_size_x):
        y = np.abs(c.map_size_y - peaks[x])
        while y < c.map_size_y:
            if map[y][x] == 0:
                holes[x] += 1

            y += 1

    return holes


def check_if_row_is_completed(map, y):
    for x in range(c.map_size_x):
        if map[y][x] == 0:
            return False

    return True


def calculate_completed_rows(map):
    completed_rows = 0
    for y in range(c.map_size_y - 1, 1, -1):
        if check_if_row_is_completed(map, y):
            completed_rows += 1

    return completed_rows


def map_to_ones(map, highest_peak):
    for row in range(c.map_size_y - 1, int(c.map_size_y - highest_peak - 1), -1):
        for col in range(c.map_size_x):
            if map[row][col] != 0:
                map[row][col] = 1
    return map


def get_row_transition(map, highest_peak):
    sum = 0
    # From highest peak to bottom
    for row in range(c.map_size_y - 1, int(c.map_size_y - highest_peak - 1), -1):
        for col in range(1, c.map_size_x):
            if map[row][col] != map[row][col - 1]:
                sum += 1
    return sum


def get_col_transition(map, peaks):
    sum = 0
    for col in range(c.map_size_x):
        if peaks[col] <= 1:
            continue
        for row in range(c.map_size_y - 1, int(c.map_size_y - peaks[col] - 1), -1):
            if map[row][col] != map[row - 1][col]:
                sum += 1
    return sum


def fitness_function(game, map):
    peaks = calculate_peaks(map)
    holes = calculate_holes(peaks, map)

    highest_peak = np.max(peaks)
    agg_height = calculate_aggregate_height(peaks)
    bumpiness = calculate_bumpiness(peaks)
    deepest_well = np.max(calculate_wells(peaks))
    num_of_pits = calculate_pits(peaks)
    num_of_holes = np.sum(holes)
    num_of_cols_with_holes = np.count_nonzero(holes)
    num_of_completed_rows = calculate_completed_rows(map)
    map_1 = map_to_ones(map, highest_peak)
    num_of_row_transitions = get_row_transition(map_1, highest_peak)
    num_of_col_transitions = get_col_transition(map_1, peaks)

    fitness_score = game.parameters[c.PARAMETERS.highest_peak_mod.value] * highest_peak + \
                    game.parameters[c.PARAMETERS.agg_height_mod.value] * agg_height + \
                    game.parameters[c.PARAMETERS.bumpiness_mod.value] * bumpiness + \
                    game.parameters[c.PARAMETERS.deepest_well_mod.value] * deepest_well + \
                    game.parameters[c.PARAMETERS.pits_mod.value] * num_of_pits + \
                    game.parameters[c.PARAMETERS.cols_with_holes_mod.value] * num_of_cols_with_holes + \
                    game.parameters[c.PARAMETERS.completed_rows_mod.value] * num_of_completed_rows + \
                    game.parameters[c.PARAMETERS.row_transitions.value] * num_of_row_transitions + \
                    game.parameters[c.PARAMETERS.col_transitions.value] * num_of_col_transitions + \
                    game.parameters[c.PARAMETERS.holes_mod.value] * num_of_holes

    return fitness_score


elitism = 0.2
mutation = 0.2


def cross(games_parameters):
    parent_1_id = np.random.randint(len(games_parameters))
    parent_2_id = np.random.randint(len(games_parameters))
    parent_1_parameters = copy.deepcopy(games_parameters[parent_1_id])
    parent_2_parameters = copy.deepcopy(games_parameters[parent_2_id])
    child_parameters = []

    for i in range(len(parent_1_parameters)):
        rand_param = np.random.choice([parent_1_parameters[i], parent_2_parameters[i]])
        child_parameters.append(rand_param)
    return child_parameters


def elitify_and_crossover(games):
    number_of_instances = np.ceil(c.games_in_x * c.games_in_y * elitism)
    best_runtime_list = sorted(games, key=lambda game: game.score, reverse=True)
    proper_parameters_list = []
    probabilities = []
    max_sum = 1
    prev_prob = 1
    for i in range(int(number_of_instances)):
        proper_parameters_list.append(copy.deepcopy(best_runtime_list[i].parameters))
        if i < number_of_instances - 1:
            prev_prob = prev_prob / 2
            probabilities.append(prev_prob)
            max_sum -= prev_prob
        else:
            probabilities.append(max_sum)

    new_games_parameters = []
    for i in range(len(games)):
        # if i >= len(best_runtime_list):
        random_params = np.random.choice(range(len(proper_parameters_list)), p=probabilities)
        new_games_parameters.append(proper_parameters_list[random_params])

    for i in range(len(games)):
        if games[i] not in proper_parameters_list:
            games[i].parameters = cross(new_games_parameters)

    return games


def mutate(games):
    for game in games:
        for parameter in range(len(game.parameters)):
            if np.random.random() <= mutation:
                game.parameters[parameter] += np.random.randn() * 0.2

    return games


def genetic_algorithm(games_list, score_sum, generation, subgenerations_to_go):
    for i in range(len(games_list)):
        games_list[i].score = score_sum[i]
        score_sum[i] = 0

    games_list = elitify_and_crossover(games_list)
    games_list = mutate(games_list)
    generation += 1
    subgenerations_to_go = 3
    subgenerations_to_go -= 1
