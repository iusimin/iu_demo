from wms.api import all as a

API_ROUTER = [
    ('/api/users/', a.UserCollectionApi),
    ('/api/login/', a.UserLoginApi),

    ('/api/inbound-parcel/inbound', a.InboundParcelResource),
    ('/api/sort_info', a.SortParcel),
    ('/api/seed-pool', a.CPSeedPool)
]

STATIC_ROUTE = [
    ('/', 'web/dist')
]