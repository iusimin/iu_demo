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
        return {
            "job_finish_datetime": "job_finish_datetime"
        }

    def get_query(self):
        return {}
    
    def transform_date(self, data):
        return [self._build_item(item) for item in data]

    def _build_item(self, item):
        item_dict = item.to_dict()
        status_text = CPSortJob.Status.get_text(item.status)
        item_dict["status_text"] = status_text
        return item_dict