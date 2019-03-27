import falcon

def login_required(req, resp, resource, params):
    session = req.context['session']
    if session.is_guest():
        raise falcon.HTTPUnauthorized('Please login')