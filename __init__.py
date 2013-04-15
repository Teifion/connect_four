from . import config

def add_views(config):
    """Pass your Configurator to this function and it will add the relevant Checker views.
    
    Something like this:
    
    from .games import connect_four
    connect_four.add_views(config)
    """
    
    # Standard views
    config.add_route('connect_four.menu', '/games/connect4/menu')
    config.add_route('connect_four.preferences', '/games/connect4/preferences')
    
    config.add_route('connect_four.game', '/games/connect4/game/{game_id}')
    config.add_route('connect_four.replay', '/games/connect4/replay/{game_id}')
    config.add_route('connect_four.new_game', '/games/connect4/new_game')
    
    # Form submitting views
    config.add_route('connect_four.make_move', '/games/connect4/make_move')
    config.add_route('connect_four.forfeit', '/games/connect4/forfeit')
    
    # Ajax views
    config.add_route('connect_four.check_turn', '/games/connect4/check_turn/{game_id}')
    
    return config
