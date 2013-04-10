"""
These functions handle talking to the database and should be considered
impure.
"""

from ..config import config

from ..models import (
    ConnectFourGame
)

import datetime
from . import logic_funcs

def find_user(identifier):
    User = config['User']
    
    print(config)
    if type(identifier) == str:
        found = config['DBSession'].query(User.id).filter(User.name == identifier).first()
        if found == None:
            return None
        return config['get_user']({'id':found[0], 'name':identifier})
    
    elif type(identifier) == int:
        found = config['DBSession'].query(User.name).filter(User.id == identifier).first()
        if found == None:
            return None
        return config['get_user']({'id':identifier, 'name':found[0]})
    
    else:
        raise KeyError("No handler for identifier type of '{}'".format(type(identifier)))

def new_game(p1, p2):
    game               = ConnectFourGame()
    game.player1       = p1.id
    game.player2       = p2.id
    game.started       = datetime.datetime.now()
    game.turn          = 0
    game.complete      = False
    game.current_state = str(logic_funcs.empty_board)
    
    config['DBSession'].add(game)
    config['DBSession'].flush()
    
    # Return the game
    return game
