import transaction
import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer

from .lib import db_funcs
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
            game = db_funcs.new_game(the_user, opponent)
            raise HTTPFound(location=request.route_url("connect_four.game", game_id=game.id))
    
    return dict(
        title        = "Connect Four",
        layout       = layout,
        the_user     = the_user,
        message      = message,
        flash_colour = flash_colour,
    )
