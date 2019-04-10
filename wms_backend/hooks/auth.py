import falcon
from wms_backend.model.mongo.rbac import Permission

def login_required(req, resp, resource, params):
    session = req.context['session']
    if session.is_guest():
        raise falcon.HTTPUnauthorized('Please login')

def permission_required(req, resp, resource, params):
    login_required(req, resp, resource, params)
    # Backdoor for stage development
    if req.context['env']['config'] == 'stage' and \
            req.headers.get('MAGIC-CODE') == 'WHOSYOURDADDY':
        return
    session = req.context['session']
    user = req.context['session'].user
    permissions = req.context['session'].permissions
    if not Permission.check_permissions(
            req.relative_uri,
            Permission.Action.name_to_num(req.method),
            permissions):
        raise falcon.HTTPForbidden('No permission to proceed')