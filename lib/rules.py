empty_board = " " * (7 * 6)

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
    for i, v in enumerate(column(current_state, col)):
        if v == " ": return True
    return False

def column(current_state, col):
    return (current_state[col + row*7] for row in range(5,-1,-1))
