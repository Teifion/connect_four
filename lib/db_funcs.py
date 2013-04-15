"""
These functions handle talking to the database and should be considered
impure.
"""

from ..config import config

from ..models import (
    ConnectFourGame
)

import datetime
from . import rules

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
    game.current_state = str(rules.empty_board)
    
    config['DBSession'].add(game)
    
    # Get game ID
    game_id = config['DBSession'].query(ConnectFourGame.id).filter(
        ConnectFourGame.player1 == p1.id,
        ConnectFourGame.player2 == p2.id,
    ).order_by(ConnectFourGame.id.desc()).first()[0]
    
    return game_id

def get_game(game_id):
    the_game = config['DBSession'].query(ConnectFourGame).filter(ConnectFourGame.id == game_id).first()
    
    if the_game == None:
        raise ValueError("We were unable to find the game")
    
    return the_game

def perform_move():
    pass
