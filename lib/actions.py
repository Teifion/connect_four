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

def set_state_by_colour(current_state, preferred_colour, player_is_player1):
    # Swap them to A and B now so we can swap them back to 1 and 2 later
    # without repeating this step
    current_state = current_state.replace("1", "A").replace("2", "B")
    
    if player_is_player1:
        if preferred_colour:
            current_state = current_state.replace("A", "1").replace("B", "2")
        else:
            current_state = current_state.replace("B", "1").replace("A", "2")
    else:
        if preferred_colour:
            current_state = current_state.replace("B", "1").replace("A", "2")
        else:
            current_state = current_state.replace("A", "1").replace("B", "2")
    
    return current_state
