# -*- coding: utf-8 -*-
from datetime import datetime

import xhtml2pdf.pisa as pisa

#from wms.api.combine_parcel.demo import DemoUtility
#from wms.model.mongo.combine_parcel.inbound_parcel import CPInboundParcel
#from wms.server import ConfigParser, IUWMSBackendService


CONFIG_FILE = '/etc/server.yml'


#def _setup():
#    options = ConfigParser.parse_config_file(CONFIG_FILE)
#    options['rate-limiter']['enable'] = False
#    application = IUWMSBackendService(options)
#    application.connect()


def generate_tracking_label(tracking_ids, output_file_name):
    html_file = '''<!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <meta charset="utf-8">
            <style type="text/css">
            @page {{ size: 10cm 6cm; }}
            @font-face {{
                font-family: 'wqynotothai';
                src: url(../../../templates/fonts/wqy_hacked.ttf);
            }}
            p {{
                font-family: 'wqynotothai';
            }}
            </style>
        </head>
        <body>
            {0}
        </body>
        </html>'''.format(
            "<br />".join(['''<div style="width:100%;text-align:center;padding-top:10px;">
                <pdf:barcode value="{0}" type="code128" align="middle"
                    barwidth="0.85" barheight="40"/>
                <p style="width:100%;text-align:center;font-size:20px;">{0}</p>
            </div>'''.format(tracking_id) for tracking_id in tracking_ids])
        )

    result_file = open(output_file_name, "w+b")
    pisa.CreatePDF(html_file, dest=result_file)


def generate_tracking_labels():
    """ parcels = CPInboundParcel.find({
        "status": {
            "$lt": CPInboundParcel.Status.Cancelled
        }
    }) """
    output_folder = "output/tracking_label"
    #tracking_ids = [parcel.tracking_id for parcel in parcels]
    prefix = "CP2019050714360"
    tracking_ids = []
    for i in range(20):
        tracking_ids.append("{0}{1:02}".format(prefix, i))
    filename = "{0}/{1}.pdf".format(output_folder,
                                    datetime.now().strftime("%Y%m%d_%H%M"))
    generate_tracking_label(tracking_ids, filename)


if __name__ == "__main__":
    #_setup()
    generate_tracking_labels()
