# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime, timedelta

import falcon
from bson import ObjectId

#import xhtml2pdf.pisa as pisa
from cl.backend.api import BaseApiResource
from cl.utils import password
from cl.utils.py_enum import PyEnumMixin
from wms.api.collection_resource import CollectionResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.model.mongo.combine_parcel.inbound_parcel import CPInboundParcel


# For demo only. Remove later.
class Demo(BaseApiResource):
    @falcon.before(login_required)
    def on_cancel_all_parcels(self, req, resp):
        DemoUtility.cancel_all_parcels()

    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      count: { type: number }
    required: [count]
    '''))
    def on_create_parcels(self, req, resp):
        count = req.media["count"]
        DemoUtility.create_inbound_parcels(count)

    @falcon.before(login_required)
    def on_inbound_all_parcels(self, req, resp):
        user = req.context['session'].user
        DemoUtility.inbound_all_parcels(user)

    @falcon.before(login_required)
    def on_set_ready_to_ship(self, req, resp):
        DemoUtility.set_ready_to_ship()

    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      job_id: { type: string }
    required: [job_id]
    '''))
    def on_run_sort_job(self, req, resp):
        job_id = req.media["job_id"]
        try:
            DemoUtility.run_sort_job(job_id)
        except InvalidOperationException as ex:
            raise falcon.HTTPBadRequest(description=str(ex))


class DemoUnCancelledParcels(CollectionResource):
    def get_query_class(self):
        return CPInboundParcel

    def get_field_mapping(self):
        return {}

    def get_query(self):
        return {
            "status": {
                "$lt": CPInboundParcel.Status.Cancelled
            }
        }

    def transform_date(self, data):
        return [self._build_item(item) for item in data]

    def _build_item(self, item):
        item_dict = item.to_dict()
        status_text = CPInboundParcel.Status.get_text(item.status)
        item_dict["status_text"] = status_text
        return item_dict


class DemoUtility(object):
    @classmethod
    def cancel_all_parcels(cls):
        CPInboundParcel.update(
            {}, {"$set": {"status": CPInboundParcel.Status.Cancelled}})

    @classmethod
    def create_inbound_parcels(cls, count):
        combine_id_count = count // 4
        tracking_prefix = "CP{0}".format(datetime.now().strftime("%Y%m%d%H%M"))
        combine_id_pool = [str(ObjectId()) for i in range(combine_id_count)]
        for i in range(count):
            combine_id = combine_id_pool[random.randint(
                0, combine_id_count - 1)]
            tracking_id = tracking_prefix + "{:03d}".format(i)

            InboundParcelUtil.create_parcel(
                tracking_id=tracking_id,
                combine_id=combine_id,
                warehouse_id="SHYW",
                inbound_carrier=0,
                latest_ship_datetime=datetime.now() + timedelta(days=random.randint(3, 5))
            )

    @classmethod
    def inbound_all_parcels(cls, user):
        inbound_parcels = CPInboundParcel.find(
            {
                "status": CPInboundParcel.Status.Pending
            }
        )

        for parcel in inbound_parcels:
            InboundParcelUtil.inbound_parcel(
                tracking_id=parcel.tracking_id,
                parcel_type=CPInboundParcel.ParcelType.Ordinary,
                weight=random.uniform(0.1, 1.2),
                has_battery=False,
                has_liquid=False,
                has_sensitive=False,
                sensitive_reason=None,
                user=user
            )

    @classmethod
    def set_ready_to_ship(cls):
        CPInboundParcel.update({
            "status": CPInboundParcel.Status.Inbound
        },
            {
            "$set": {
                "ready_to_ship": True,
                "updated_datetime": datetime.utcnow()
            }
        })

    @classmethod
    def run_sort_job(cls, job_id):
        SortJobUtil.allocate_cabinet_for_parcels(job_id)

    #@classmethod
    #def generate_tracking_label(cls, tracking_ids, output_file_name):
    #    html_file = '''<!DOCTYPE html>
    #        <html xmlns="http://www.w3.org/1999/xhtml">
    #        <head>
    #            <meta http-equiv="content-type" content="text/html; charset=utf-8">
    #            <meta charset="utf-8">
    #            <style type="text/css">
    #            @page {{ size: 10cm 6cm; }}
    #            @font-face {{
    #                font-family: 'wqynotothai';
    #                src: url(/fonts/wqy_hacked.ttf);
    #            }}
    #            p {{
    #                font-family: 'wqynotothai';
    #            }}
    #            </style>
    #        </head>
    #        <body>
    #            {0}
    #        </body>
    #        </html>'''.format(
    #            "<br />".join(['''<div style="width:100%;text-align:center;padding-top:10px;">
    #                <pdf:barcode value="{0}" type="code128" align="middle"
    #                    barwidth="0.85" barheight="40"/>
    #                <p style="width:100%;text-align:center;font-size:20px;">{0}</p>
    #            </div>''' for tracking_id in tracking_ids])
    #        )

    #    result_file = open(output_file_name, "w+b")
    #    pisa.CreatePDF(html_file, dest=result_file)
