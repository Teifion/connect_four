from pyramid.httpexceptions import HTTPFound

def forward_to_game(request, data):
    game_id = int(data)
    return HTTPFound(location=request.route_url('connect_four.game', game_id=game_id))

def forward_to_profile(request, data):
    return HTTPFound(location=request.route_url('connect_four.stats'))
