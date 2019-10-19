from wms.api import all as a

API_ROUTER = [
    ('/api/roles/', a.RoleCollectionApi),
    ('/api/role/{role_id}/', a.RoleApi),
    ('/api/role/{role_id}/permissions/', a.RolePermissionCollectionApi),
    ('/api/role/{role_id}/permission/{permission_id:int}/', a.RolePermissionApi),
    ('/api/role/{role_id}/parents/', a.RoleParentCollectionApi),
    ('/api/role/{role_id}/parent/{parent_name}/', a.RoleParentApi),

    ('/api/users/', a.UserCollectionApi),
    ('/api/login/', a.UserLoginApi),
    ('/api/operator-warehouse', a.OperatorWarehouse),

    ('/api/inbound-parcel/{tracking_id}', a.InboundParcelResource),
    ('/api/inbound-parcels', a.InboundParcelCombineResource),
    ('/api/sort-info', a.SortParcel),
    ('/api/seed-pool', a.CPSeedPool),
    ('/api/sort-job', a.SortJob),
    ('/api/sort-jobs', a.CPSortJobCollectionResource),
    ('/api/sort-pool-parcels', a.CPSortPoolCollectionResource),
    ('/api/active-sort-job', a.ActiveSortJob),

    # For demo only. Remove later.
    ('/api/demo', a.Demo),
    ('/api/demo/uncancelled-parcels', a.DemoUnCancelledParcels)
]

STATIC_ROUTE = [
    ('/', 'web/dist')
]