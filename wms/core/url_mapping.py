from wms.api import all as a

API_ROUTER = [
    ('/api/users/', a.UserCollectionApi),
    ('/api/login/', a.UserLoginApi),

    ('/api/inbound-parcel/inbound', a.InboundParcelResource),
    ('/api/sort-info', a.SortParcel),
    ('/api/seed-pool', a.CPSeedPool),
    ('/api/sort-job', a.SortJob),
    ('/api/sort-jobs', a.CPSortJobCollectionResource),
    ('/api/sort-pool-parcels', a.CPSortPoolCollectionResource)
]

STATIC_ROUTE = [
    ('/', 'web/dist')
]