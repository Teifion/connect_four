import transaction
import datetime

from pyramid.view import view_config
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

from .config import config

@view_config(route_name='connect_four.menu', renderer='templates/menu.pt', permission='loggedin')
def menu(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer('../../templates/layouts/viewer.pt').implementation()
    
    game_list = []
    
    return dict(
        title      = "Connect Four",
        layout     = layout,
        the_user   = the_user,
        
        game_list  = game_list
    )

@view_config(route_name='connect_four.new_game', renderer='templates/new_game.pt', permission='loggedin')
def new_game(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer('../../templates/layouts/viewer.pt').implementation()
    
    message = ""
    flash_colour = "A00"
    
    if "form.submitted" in request.params:
        opponent_name = request.params['opponent_name'].strip().upper()
        opponent = db_funcs.find_user(opponent_name)
        
        # Failure :(
        if opponent == None:
            message = """I'm sorry, we cannot find any opponent by the name of '{}'""".format(opponent_name)
            
        else:
            game_id = db_funcs.new_game(the_user, opponent)
            return HTTPFound(location=request.route_url("connect_four.game", game_id=game_id))
    
    return dict(
        title        = "Connect Four",
        layout       = layout,
        the_user     = the_user,
        message      = message,
        flash_colour = flash_colour,
    )

@view_config(route_name='connect_four.game', renderer='templates/view_game.pt', permission='loggedin')
def view_game(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer('../../templates/layouts/viewer.pt').implementation()
    
    game_id  = int(request.matchdict['game_id'])
    the_game = db_funcs.get_game(game_id)
    message  = ""
    
    return dict(
        title    = "Connect Four",
        layout   = layout,
        the_user = the_user,
        the_game = the_game,
        message  = message,
    )

@view_config(route_name='connect_four.make_move', renderer='templates/make_move.pt', permission='loggedin')
def make_move(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer('../../templates/layouts/viewer.pt').implementation()
    
    message = ""
    flash_colour = "A00"
    
    game_id  = int(request.params['game_id'])
    column   = int(request.params['column'])
    
    the_game = db_funcs.get_game(game_id)
    current_player = rules.current_player(the_game)
    
    if current_player == the_user.id:
        try:
            actions.perform_move(the_game, column)
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
