# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.utils import password
from wms.api import BaseApiResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.model.mongo.user import User
from wms.model.redis_keys.session import Session


class SortParcel(BaseApiResource):
    #@falcon.before(login_required)
    def on_get(self, req, resp):
        tracking_id = req.get_param("tracking_id", required=True)
        job_id = req.get_param("job_id", required=True)
        round_id = req.get_param_as_int("round_id", required=True)

        sort_info = SortJobUtil.get_parcel_sort_info(job_id, tracking_id, round_id)

        resp.media = {
            "sort_info": sort_info
        }
