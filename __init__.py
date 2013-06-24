from . import views

def includeme(config):
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
