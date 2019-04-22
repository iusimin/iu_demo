# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon
from cl.backend.api import BaseApiResource
from cl.utils import password
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.data_accessor.sort_job_accessor import \
    SortJobAccessor
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.model.mongo.combine_parcel.inbound_parcel import CPInboundParcel
from wms.model.mongo.user import User
from wms.model.redis_keys.session import Session


class SortParcel(BaseApiResource):
    @falcon.before(login_required)
    def on_get(self, req, resp):
        tracking_id = req.get_param("tracking_id", required=True)
        job_id = req.get_param("job_id", required=True)
        round_id = req.get_param_as_int("round_id", required=True)

        try:
            sort_info = SortJobUtil.get_parcel_sort_info(job_id, tracking_id, round_id)
        except ValueError as ex:
            raise falcon.HTTPNotFound(description=str(ex))

        parcel = CPInboundParcel.by_tracking_id(tracking_id)
        sort_info["weight"] = parcel.weight
        sort_info["inbound_datetime"] = parcel.timeline.inbound.strftime("%Y-%m-%d %H:%M:%S")

        resp.media = {
            "sort_info": sort_info
        }
