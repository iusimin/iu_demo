from web_backend.api import all as a

API_ROUTER = [
    ('/api/users/', a.UserCollectionApi),
    ('/api/user/{user_id}/', a.UserApi),
    ('/api/user/{user_id}/roles/', a.UserRoleCollectionApi),
    ('/api/user/{user_id}/role/{role_name}/', a.UserRoleApi),
    ('/api/user/{user_id}/permissions/', a.UserPermissionCollectionApi),
    ('/api/user/{user_id}/permission/{permission_id:int}/', a.UserPermissionApi),
    ('/api/demo/', a.DemoApi),
    ('/api/login/', a.UserLoginApi),
    ('/api/session/', a.SessionCollectionApi),
    ('/api/roles/', a.RoleCollectionApi),
    ('/api/role/{role_name}/', a.RoleApi),
    ('/api/role/{role_name}/permissions/', a.RolePermissionCollectionApi),
    ('/api/role/{role_name}/permission/{permission_id:int}/', a.RolePermissionApi),
    ('/api/role/{role_name}/parents/', a.RoleParentCollectionApi),
    ('/api/role/{role_name}/parent/{parent_name}/', a.RoleParentApi),
]