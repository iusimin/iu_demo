# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.utils import password
from wms_backend.api import BaseApiResource
from wms_backend.hooks.auth import login_required, permission_required
from wms_backend.hooks.validation import JsonSchema
from wms_backend.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms_backend.lib.combine_parcel.utilities.sort_job_util import SortJobUtil
from wms_backend.lib.exception.exception import InvalidOperationException
from wms_backend.model.mongo.user import User
from wms_backend.model.redis_keys.session import Session


class CPSeedPool(BaseApiResource):

    def on_get(self, req, resp):
        tracking_id = req.get_param("tracking_id", required=True)
        job_id = req.get_param("job_id", required=True)

        parcels = SortJobUtil.get_combine_cabinet_from_first_tracking_id(job_id, tracking_id)

        resp.media = {
            "parcels": parcels
        }
