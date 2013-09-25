def connect4_nimblescan():
    try:
        from ...nimblescan import api
    except ImportError:
        try:
            from ..nimblescan import api
        except ImportError:
            return
    
    api.register('connect_four.menu', "Connect 4 - Menu", ['games'], (lambda r: True), api.make_forwarder("connect_four.menu"))
    api.register('connect_four.new_game', "Connect 4 - New game", ['games'], (lambda r: True), api.make_form_forwarder("connect_four.new_game", []), '<label for="ns_opponent">Opponent:</label> <input type="text" name="opponent_name" id="ns_opponent" value="" style="display:inline-block;"/>')
    api.register('connect_four.stats', "Connect 4 - Stats", ['games'], (lambda r: True), api.make_forwarder("connect_four.stats"))
    api.register('connect_four.preferences', "Connect 4 - Preferences", ['games'], (lambda r: True), api.make_forwarder("connect_four.preferences"))

def connect4_notifications():
    try:
        from ...communique import register, send
    except ImportError:
        try:
            from ..communique import register, send
        except ImportError:
            return
    
    from .lib.notifications import forward_to_game, forward_to_profile
    
    register('connect_four.new_game', 'New game', 'http://localhost:6543/static/images/communique/connect4.png', forward_to_game)
    register('connect_four.new_move', 'New move', 'http://localhost:6543/static/images/communique/connect4.png', forward_to_game)
    register('connect_four.end_game', 'Game over', 'http://localhost:6543/static/images/communique/connect4.png', forward_to_game)
    register('connect_four.win_game', 'Victory!', 'http://localhost:6543/static/images/communique/connect4.png', forward_to_game)

def includeme(config):
    from . import views
    
    connect4_notifications()
    connect4_nimblescan()
    
    """
    Pass this to your configurator object like so:
    
    from . import connect_four
    config.include(connect_four, route_prefix="games/connect4")
    """
    
    # Standard views
    config.add_route('connect_four.menu', '/menu')
    config.add_route('connect_four.preferences', '/preferences')
    config.add_route('connect_four.stats', '/stats')
    config.add_route('connect_four.head_to_head_stats', '/head_to_head_stats')
    
    config.add_route('connect_four.game', '/game/{game_id}')
    config.add_route('connect_four.replay', '/replay/{game_id}')
    config.add_route('connect_four.new_game', '/new_game')
    
    # Form submitting views
    config.add_route('connect_four.make_move', '/make_move')
    config.add_route('connect_four.forfeit', '/forfeit')
    
    # Ajax views
    config.add_route('connect_four.check_turn', '/check_turn/{game_id}')
    config.add_route('connect_four.rematch', '/rematch/{game_id}')
    
    # Now link the views
    config.add_view(views.menu, route_name='connect_four.menu', renderer='templates/menu.pt', permission='loggedin')
    config.add_view(views.stats, route_name='connect_four.stats', renderer='templates/stats.pt', permission='loggedin')
    config.add_view(views.head_to_head_stats, route_name='connect_four.head_to_head_stats', renderer='templates/head_to_head_stats.pt', permission='loggedin')
    config.add_view(views.preferences, route_name='connect_four.preferences', renderer='templates/preferences.pt', permission='loggedin')
    config.add_view(views.new_game, route_name='connect_four.new_game', renderer='templates/new_game.pt', permission='loggedin')
    config.add_view(views.view_game, route_name='connect_four.game', renderer='templates/view_game.pt', permission='loggedin')
    config.add_view(views.make_move, route_name='connect_four.make_move', renderer='templates/make_move.pt', permission='loggedin')
    config.add_view(views.rematch, route_name='connect_four.rematch', renderer='string', permission='loggedin')
    config.add_view(views.check_turn, route_name='connect_four.check_turn', renderer='string', permission='loggedin')
    
    return config
