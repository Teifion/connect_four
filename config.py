class AUser(object):
    """A simple object to provide an interface into whatever your system User object is.
    It allows us to use property names within the Connect Four framework without having
    to know what your User object uses."""
    
    def __init__(self, request_object):
        super(AUser, self).__init__()
        
        if type(request_object) == dict:
            return self.__from_dict(request_object)
        
        user_object = config['get_user_func'](request_object)
        self.id   = getattr(user_object, config['user.id_property'])
        self.name = getattr(user_object, config['user.name_property'])
    
    def __from_dict(self, dict_oject):
        self.id   = dict_oject['id']
        self.name = dict_oject['name']

config = {
    "layout": "../templates/default_layout.pt",
    "DBSession": None,
    "User": None,
    "use_achievements": False,
    
    "get_user_func": lambda r: KeyError("No function exists to get the user"),
    "get_user": AUser,
    
    # I use this at work so it's an opportunity to check that the user's not been blocked
    "check_blocked": lambda r: None,
}

# This is a copy of how I'm setting up my Connect Four configuration  
# from .games import connect_four
# config.include(connect_four, route_prefix="games/connect4")
# connect_four.config.config['layout'] = '../templates/layouts/viewer.pt'
# connect_four.config.config['DBSession'] = DBSession
# connect_four.config.config['User'] = models.User
# 
# connect_four.config.config['get_user_func']      = lambda r: r.user
# connect_four.config.config['user.id_property']   = "id"
# connect_four.config.config['user.name_property'] = "name"
# 
# def _game_check(request):
#     if request.user.blocked: raise HTTPFound(location="/")
# connect_four.config.config['check_blocked'] = _game_check