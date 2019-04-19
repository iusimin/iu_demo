# -*- coding: utf-8 -*-

import falcon

from wms.api.collection_resource import CollectionResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.model.mongo.combine_parcel.sort_job import CPSortJob


class CPSortJobCollectionResource(CollectionResource):
    def get_query_class(self):
        return CPSortJob

    def get_field_mapping(self):
        return {}

    def get_query(self):
        return {}
    
    def transform_date(self, data):
        return data
