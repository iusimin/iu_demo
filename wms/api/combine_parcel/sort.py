# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.utils import password
from wms.api import BaseApiResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.data_accessor.sort_job_accessor import \
    SortJobAccessor
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.model.mongo.sequence_id_generator import SequenceIdGenerator
from wms.model.mongo.user import User
from wms.model.redis_keys.session import Session
from wms.tasks.combine_parcel.sort_job_task import CPSortJobTasks


class SortParcel(BaseApiResource):
    #@falcon.before(login_required)
    def on_get(self, req, resp):
        tracking_id = req.get_param("tracking_id", required=True)
        job_id = req.get_param("job_id", required=True)
        round_id = req.get_param_as_int("round_id", required=True)

        try:
            sort_info = SortJobUtil.get_parcel_sort_info(job_id, tracking_id, round_id)
        except ValueError as ex:
            raise falcon.HTTPNotFound(description=str(ex))

        resp.media = {
            "sort_info": sort_info
        }

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
