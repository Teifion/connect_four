def includeme(config):
    """
    Pass this to your configurator object like so:
    
    from . import connect_four
    config.include(connect_four)
    """
    
    # Standard views
    config.add_route('connect_four.menu', '/connect4/menu')
    config.add_route('connect_four.preferences', '/connect4/preferences')
    config.add_route('connect_four.stats', '/connect4/stats')
    config.add_route('connect_four.head_to_head_stats', '/connect4/head_to_head_stats')
    
    config.add_route('connect_four.game', '/connect4/game/{game_id}')
    config.add_route('connect_four.replay', '/connect4/replay/{game_id}')
    config.add_route('connect_four.new_game', '/connect4/new_game')
    
    # Form submitting views
    config.add_route('connect_four.make_move', '/connect4/make_move')
    config.add_route('connect_four.forfeit', '/connect4/forfeit')
    
    # Ajax views
    config.add_route('connect_four.check_turn', '/connect4/check_turn/{game_id}')
    config.add_route('connect_four.rematch', '/connect4/rematch/{game_id}')
    
    # Now add the views
    config.add_view(route_name='connect_four.menu', renderer='templates/menu.pt', permission='loggedin')
    config.add_view(route_name='connect_four.stats', renderer='templates/stats.pt', permission='loggedin')
    config.add_view(route_name='connect_four.head_to_head_stats', renderer='templates/head_to_head_stats.pt', permission='loggedin')
    config.add_view(route_name='connect_four.preferences', renderer='templates/preferences.pt', permission='loggedin')
    config.add_view(route_name='connect_four.new_game', renderer='templates/new_game.pt', permission='loggedin')
    config.add_view(route_name='connect_four.game', renderer='templates/view_game.pt', permission='loggedin')
    config.add_view(route_name='connect_four.make_move', renderer='templates/make_move.pt', permission='loggedin')
    config.add_view(route_name='connect_four.rematch', renderer='string', permission='loggedin')
    config.add_view(route_name='connect_four.check_turn', renderer='string', permission='loggedin')
    
    return config
