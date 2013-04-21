"""
These functions handle talking to the database and should be considered
impure.
"""

from ..config import config

from ..models import (
    ConnectFourGame,
    ConnectFourMove,
    ConnectFourProfile,
)

from sqlalchemy import or_, and_
import datetime
from . import rules
from . import actions

def get_profile(user_id):
    the_profile = config['DBSession'].query(ConnectFourProfile).filter(ConnectFourProfile.user == user_id).first()
    
    if the_profile is None:
        the_profile = add_empty_profile(user_id)
    
    return the_profile

def add_empty_profile(user_id):
    the_profile = ConnectFourProfile()
    the_profile.user = user_id
    
    config['DBSession'].add(the_profile)
    return the_profile

def get_game_list(user_id):
    "Games waiting for us to make our move"
    User = config['User']
    
    filters = (
        or_(
            and_(ConnectFourGame.player1 == user_id, "mod(connect_four_games.turn, 2) = 0", User.id == ConnectFourGame.player2),
            and_(ConnectFourGame.player2 == user_id, "mod(connect_four_games.turn, 2) = 1", User.id == ConnectFourGame.player1),
        ),
        ConnectFourGame.winner == None,
    )
    
    return list(config['DBSession'].query(ConnectFourGame.id, User.name, ConnectFourGame.turn).filter(*filters))

def get_waiting_game_list(user_id):
    "Games waiting for our opponent to make a move"
    User = config['User']
    
    filters = (
        or_(
            and_(ConnectFourGame.player1 == user_id, "mod(connect_four_games.turn, 2) = 1", User.id == ConnectFourGame.player2),
            and_(ConnectFourGame.player2 == user_id, "mod(connect_four_games.turn, 2) = 0", User.id == ConnectFourGame.player1),
        ),
        ConnectFourGame.winner == None,
    )
    
    return list(config['DBSession'].query(ConnectFourGame.id, User.name, ConnectFourGame.turn).filter(*filters))

def get_recent_game_list(user_id, limit=5):
    "The most recently completed games, we return the id of the winner as a 4th attribute"
    User = config['User']
    
    filters = (
        or_(
            and_(ConnectFourGame.player1 == user_id, User.id == ConnectFourGame.player2),
            and_(ConnectFourGame.player2 == user_id, User.id == ConnectFourGame.player1),
        ),
        ConnectFourGame.winner != None,
    )
    
    return list(config['DBSession'].query(
        ConnectFourGame.id, User.name, ConnectFourGame.turn, ConnectFourGame.winner
    ).filter(*filters).order_by(ConnectFourGame.id.desc()).limit(limit))

def find_user(identifier):
    User = config['User']
    
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

def new_game(p1, p2, rematch=None):
    game               = ConnectFourGame()
    game.player1       = p1.id
    game.player2       = p2.id
    game.started       = datetime.datetime.now()
    game.turn          = 0
    game.source        = rematch
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

def add_turn(the_game, column):
    new_turn           = ConnectFourMove()
    new_turn.game      = the_game.id
    new_turn.player    = rules.current_player(the_game)
    
    new_turn.move      = column
    new_turn.timestamp = datetime.datetime.now()
    
    config['DBSession'].add(new_turn)

def end_game(the_game):
    the_game.complete = True
    
    current_player = rules.current_player_number(the_game.turn)
    the_game.winner = rules.get_player_user_id(the_game, 3-current_player)
    
def draw_game(the_game):
    the_game.complete = True
    the_game.winner = -1

def perform_move(the_game, column):
    add_turn(the_game, column)
    actions.perform_move(the_game, column)
    actions.increment_turn(the_game)
    
    end_result = rules.check_for_game_end(the_game.current_state)
    if end_result == True:
        end_game(the_game)
    elif end_result == None:
        draw_game(the_game)
    
    config['DBSession'].add(the_game)
