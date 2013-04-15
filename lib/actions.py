from . import rules

def perform_move(the_game, col):
    row = rules.first_empty(rules.column(the_game.current_state, col))
    position = rules.get_place_position(row, col)
    player_number = rules.current_player_number(the_game.turn)
    the_game.current_state = update_game(the_game.current_state, position, player_number)

def update_game(current_state, position, value):
    a = list(current_state)
    a[position] = str(value)
    return "".join(a)

def increment_turn(the_game):
    the_game.turn += 1
