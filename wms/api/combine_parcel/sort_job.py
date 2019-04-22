# -*- coding: utf-8 -*-

import falcon
from cl.backend.api import BaseApiResource
from wms.api.collection_resource import CollectionResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.data_accessor.sort_job_accessor import \
    SortJobAccessor
from wms.model.mongo.combine_parcel.combine_pool import CPSortPool
from wms.model.mongo.combine_parcel.sort_job import CPSortJob


class SortJob(BaseApiResource):
    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      job_type: { type: number }
    required: [job_type]
    '''))
    def on_post(self, req, resp):
        session = req.context['session']
        user = session.user
        warehouse_id = user.warehouse_id

        params = req.media
        job_type = params['job_type']

        job_prefix = warehouse_id + datetime.utcnow().strftime("%Y%m%d")
        job_id = SequenceIdGenerator.get_sequence_id(job_prefix)

        job = SortJobAccessor.create_if_no_running(job_id, job_type, warehouse_id)

        if job:
            resp.media = {
                "job_id": job_id
            }
            CPSortJobTasks.run_job.delay(job_id)
        else:
            raise falcon.HTTPBadRequest(description="No job was create.")

    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      job_id: { type: string }
    required: [job_id]
    ''',
    target="params"))
    def on_get(self, req, resp):
        job_id = req.get_param("job_id", required=True)
        accessor = SortJobAccessor(job_id)

        job = accessor.sort_job
        resp.media = {
            "job_detail": job.to_dict()
        }


class CPSortPoolCollectionResource(CollectionResource):
    def get_query_class(self):
        CPSortPool

    def get_field_mapping(self):
        return {
            "job_id": "job_id"
        }

    def get_query(self):
        job_id = self.query_dict.get("job_id")
        if not job_id:
            raise falcon.HTTPNotFound()
        return {
            "job_id": job_id
        }

    def transform_date(self, data):
        return [self._build_item(item) for item in data]

    def _build_item(self, item):
        item_dict = item.to_dict()
        sort_type_text = CPSortPool.SortType.get_text(item.sort_type)
        item_dict["sort_type_text"] = sort_type_text
        return item_dict


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
        job_ids = [item.job_id for item in data]
        parcel_count = SortJobAccessor.get_job_parcel_count(job_ids)
        return [self._build_item(item, parcel_count) for item in data]

    def _build_item(self, item, parcel_count):
        item_dict = item.to_dict()
        status_text = CPSortJob.Status.get_text(item.status)
        item_dict["status_text"] = status_text
        item_dict["parcel_count"] = parcel_count.get(item.job_id, 0)
        return item_dict
