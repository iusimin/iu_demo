from wms.api import all as a

API_ROUTER = [
    ('/api/inbound-parcel/inbound', a.InboundParcelResource),
    ('/api/seed-pool', a.CPSeedPool)
]