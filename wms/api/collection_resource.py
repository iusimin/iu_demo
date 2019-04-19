# -*- coding: utf-8 -*-

import falcon

from cl.backend.api import BaseApiResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema

class CollectionResource(BaseApiResource):
    DEFAULT_PAGE_SIZE = 30
    
    #TODO antony: refactor, put validation in derived class
    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      pagination: { type: object }
    required: [pagination]
    '''))
    def on_get(self, req, resp):
        pagination = req.media["pagination"]

        skip, limit = self.get_range(pagination)

        mongo_cls = self.get_query_class()
        query = self.get_query()
        sort = self.get_sort(pagination)

        data = mongo_cls.find(
            query,
            sort=sort or None,
            skip=skip,
            limit=limit
        )
        total_count = mongo_cls.count(query)

        data = self.transform_date(data)

        resp.media = {
            "data": data,
            "total_count": total_count
        }

    def get_query_class(self):
        raise NotImplementedError()

    def get_field_mapping(self):
        return {}

    def get_query(self):
        return {}

    def get_range(self, pagination):
        page = pagination.get("page", 1)
        pageSize = pagination.get("rowsPerPage", CollectionResource.DEFAULT_PAGE_SIZE)
        skip = (page - 1) * pageSize
        limit = pageSize
        return skip, limit

    def get_sort(self, pagination):
        mapping = self.get_field_mapping()
        sort = []
        if pagination:
            sortBy = pagination.get("sortBy")
            descending = pagination.get("descending", False)
            if sortBy:
                sort = [(mapping[sortBy], -1 if descending else 1)]

        return sort

    def transform_date(self, data):
        return data
