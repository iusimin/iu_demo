# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.backend.api import BaseApiResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil


class CPSeedPool(BaseApiResource):
    @falcon.before(login_required)
    def on_get(self, req, resp):
        tracking_id = req.get_param("tracking_id", required=True)
        job_id = req.get_param("job_id", required=True)

        parcels = SortJobUtil.get_combine_cabinet_from_first_tracking_id(job_id, tracking_id)

        resp.media = {
            "parcels": parcels
        }
