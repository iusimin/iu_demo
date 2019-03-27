from web_backend.model.redis_keys.session import Session

class SessionMiddleware(object):
    def process_request(self, req, resp):
        ''' Assign a server-side session for each access
        '''
        cookies = req.cookies
        session_id = cookies.get('session_id')
        if session_id is None:
            session_id = Session.create_new_session()
            resp.set_cookie('session_id', session_id)
        session = Session(session_id)
        if not session.is_valid():
            # Session expired
            session_id = Session.create_new_session()
            resp.set_cookie('session_id', session_id)
        req.context['session'] = session