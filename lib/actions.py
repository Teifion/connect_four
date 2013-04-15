from . import rules

def perform_move(the_game, column):
    print("\n\n")
    print(list(rules.column(the_game.current_state, column)))
    print("\n\n")
    
    if not rules.is_move_valid(column, the_game.current_state):
        raise Exception("Invalid move")
    
    return True
