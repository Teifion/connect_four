import transaction
import datetime
from datetime import timedelta

from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer

from .lib import (
    db_funcs,
    actions,
    rules,
)

from .models import (
    ConnectFourGame,
    ConnectFourMove,
)

try:
    try:
        from ...communique import send as com_send
    except ImportError:
        try:
            from ..communique import send as com_send
        except ImportError:
            raise
except Exception as e:
    raise
    def com_send(*args, **kwargs):
        pass

from .config import config

def menu(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    # We call but don't query this so that we can assign a profile
    # if none exists
    db_funcs.get_profile(the_user.id)
    
    game_list    = db_funcs.get_game_list(the_user.id)
    waiting_list = db_funcs.get_waiting_game_list(the_user.id)
    recent_list  = db_funcs.get_recent_game_list(the_user.id)
    
    return dict(
        title        = "Connect Four",
        layout       = layout,
        the_user     = the_user,
        
        game_list    = game_list,
        waiting_list = waiting_list,
        recent_list  = recent_list,
    )

def stats(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    db_funcs.get_profile(the_user.id)
    layout = get_renderer(config['layout']).implementation()
    
    stats = db_funcs.get_stats(the_user.id)
    
    return dict(
        title    = "Connect Four stats",
        layout   = layout,
        the_user = the_user,
        
        stats    = stats,
    )

def head_to_head_stats(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    message  = ""
    
    if "opponent_name" in request.params:
        opponent_name = request.params['opponent_name'].strip().upper()
        opponent = db_funcs.find_user(opponent_name)
        
    else:
        opponent_id = int(request.params['opponent_id'])
        opponent = db_funcs.find_user(opponent_id)
    
    stats = None
        
    if opponent is not None:
        stats = db_funcs.get_stats(the_user.id, opponent.id)
    else:
        message = "No opponent could be found"
    
    return dict(
        stats    = stats,
        message  = message,
        opponent = opponent,
    )

def preferences(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    profile = db_funcs.get_profile(the_user.id)
    layout = get_renderer(config['layout']).implementation()
    message = ""
    
    if "preferred_colour" in request.params:
        preferred_colour = request.params['preferred_colour']
        if preferred_colour == "true":
            profile.preferred_colour = True
        else:
            profile.preferred_colour = False
        
        message = "Changes saved"
    
    return dict(
        title    = "Connect Four preferences",
        layout   = layout,
        the_user = the_user,
        profile  = profile,
        message  = message,
    )

def new_game(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    message = ""
    flash_colour = "A00"
    
    if "opponent_name" in request.params:
        opponent_name = request.params['opponent_name'].strip().upper()
        opponent = db_funcs.find_user(opponent_name)
        
        # Failure :(
        if opponent == None:
            message = """I'm sorry, we cannot find any opponent by the name of '{}'""".format(opponent_name)
            
        else:
            game_id = db_funcs.new_game(the_user, opponent)
            com_send(opponent.id, "connect_four.new_game", "{} has started a game against you".format(the_user.name), str(game_id), timedelta(hours=24))
            return HTTPFound(location=request.route_url("connect_four.game", game_id=game_id))
    
    return dict(
        title        = "Connect Four",
        layout       = layout,
        the_user     = the_user,
        message      = message,
        flash_colour = flash_colour,
    )

def view_game(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    profile = db_funcs.get_profile(the_user.id)
    layout = get_renderer(config['layout']).implementation()
    
    game_id  = int(request.matchdict['game_id'])
    the_game = db_funcs.get_game(game_id)
    message  = ""
    
    if the_game.player1 == the_user.id:
        opponent = db_funcs.find_user(the_game.player2)
        game_state = actions.set_state_by_colour(the_game.current_state, profile.preferred_colour, player_is_player1=True)
    else:
        opponent = db_funcs.find_user(the_game.player1)
        game_state = actions.set_state_by_colour(the_game.current_state, profile.preferred_colour, player_is_player1=False)
    
    winner = None
    if the_game.winner != None:
        winner = db_funcs.find_user(the_game.winner)
    
    return dict(
        title       = "Connect Four: {}".format(opponent.name),
        layout      = layout,
        the_user    = the_user,
        the_game    = the_game,
        your_turn   = rules.current_player(the_game) == the_user.id,
        profile     = profile,
        winner      = winner,
        message     = message,
        positions   = rules.visual_positions(),
        valid_moves = list(rules.valid_moves(the_game.current_state)),
        opponent    = opponent,
        game_state  = game_state,
    )

def make_move(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    message = ""
    flash_colour = "A00"
    
    game_id  = int(request.params['game_id'])
    column   = int(request.params['column'])
    
    the_game = db_funcs.get_game(game_id)
    current_player = rules.current_player(the_game)
    
    if the_game.winner not in (None, -1):
        message = "The game is over"
    
    elif current_player == the_user.id:
        try:
            if not rules.is_move_valid(the_game.current_state, column):
                raise Exception("Invalid move")
            
            db_funcs.perform_move(the_game, column)
            com_send(rules.current_player(the_game), "connect_four.new_move", "{} has made a move".format(the_user.name), str(game_id), timedelta(hours=24))
            
            return HTTPFound(location=request.route_url("connect_four.game", game_id=game_id))
        except Exception as e:
            message = e.args[0]
    else:
        message = "It is not your turn"
    
    return dict(
        title        = "Connect Four",
        layout       = layout,
        the_user     = the_user,
        the_game     = the_game,
        message      = message,
        flash_colour = flash_colour,
    )

def rematch(request):
    config['check_blocked'](request)
    the_user = config['get_user_func'](request)
    game_id  = int(request.matchdict['game_id'])
    the_game = db_funcs.get_game(game_id)
    
    # Not a player? Send them back to the menu
    if the_user.id != the_game.player1 and the_user.id != the_game.player2:
        return HTTPFound(location=request.route_url("connect_four.menu"))
    
    # Not over yet? Send them back to the game in question.
    if the_game.winner == None:
        return HTTPFound(location=request.route_url("connect_four.game", game_id=game_id))
    
    if the_user.id == the_game.player1:
        opponent = db_funcs.find_user(the_game.player2)
    else:
        opponent = db_funcs.find_user(the_game.player1)
    
    newgame_id = db_funcs.new_game(the_user, opponent, rematch=game_id)
    the_game.rematch = newgame_id
    
    # com_send(opponent.id, "connect_four.new_game", "{} has started a game against you".format(the_user.name), str(newgame_id), timedelta(hours=24))
    return HTTPFound(location=request.route_url("connect_four.game", game_id=newgame_id))
    

def check_turn(request):
    config['check_blocked'](request)
    request.do_not_log = True
    
    the_user = config['get_user_func'](request)
    game_id  = int(request.matchdict['game_id'])
    
    the_game = db_funcs.get_game(game_id)
    if rules.current_player(the_game) == the_user.id:
        return "True"
    return "False"
