width = 7
height = 6
empty_board = " " * (width * height)

def get_player_user_id(the_game, player_number):
    if player_number == 1: return the_game.player1
    if player_number == 2: return the_game.player2
    raise KeyError("There is no player of {}".format(player_number))

def get_player_game_number(the_game, player_id):
    if the_game.player1 == player_id: return 1
    if the_game.player2 == player_id: return 2
    raise KeyError("None of the players have an ID of {}".format(player_id))

def current_player(the_game):
    return get_player_user_id(the_game, current_player_number(the_game.turn))

def current_player_number(game_turn):
    if game_turn % 2 == 0: return 1
    else: return 2

def is_move_valid(current_state, col):
    return first_empty(column(current_state, col)) is not None

def column(current_state, col):
    return (current_state[col + row*width] for row in range(height))

def first_empty(column_sequence):
    for i, v in enumerate(column_sequence):
        if v == " ": return i
    return None

def get_place_position(row, col):
    return (row * width) + col

def visual_positions():
    for row in range(height):
        for col in range(width):
            yield get_place_position(5-row, col)

def _update_reader(reader, new_square):
    if reader == [] or new_square == " ":
        return [new_square]
    
    if new_square == reader[0]:
        if len(reader) == 3:
            return True
        return reader + [new_square]
    else:
        return [new_square]

def _check_horrizontal_end(current_state):
    for row in range(height):
        reader = []
        for col in range(width):
            reader = _update_reader(reader, current_state[get_place_position(row, col)])
            
            if reader is True:
                return True

def _check_vertical_end(current_state):
    for col in range(width):
        reader = []
        for row in range(height):
            reader = _update_reader(reader, current_state[get_place_position(row, col)])
            
            if reader is True:
                return True

def check_for_game_end(current_state):
    # First we want to check to see horrizontals
    function_list = (
        _check_horrizontal_end,
        _check_vertical_end,
    )
    
    for f in function_list:
        if f(current_state) is True:
            return True
    
    return False