
from datetime import datetime

from wms.lib.accessor_base import AccessorBase
from wms.model.mongo.warehouse import Warehouse, CPCabinetSize


class WarehouseAccessor(AccessorBase):
    def __init__(self, warehouse_id):
        if not warehouse_id:
            raise ValueError("warehouse_id")
            
        self.warehouse = Warehouse.by_warehouse_id(warehouse_id)

        if not self.warehouse:
            raise ValueError("warehouse_id")

    def update_setting(self, cabinet_count, cabinet_size, cabinet_orientation, weight_unit):
        self.warehouse.cabinet_count = cabinet_count
        self.warehouse.cabinet_orientation = cabinet_orientation
        self.warehouse.weight_unit = weight_unit
        self.warehouse.cabinet_size = CPCabinetSize(
            width = cabinet_size["width"],
            height = cabinet_size["height"]
        )

    def flush(self, transaction_session=None):
        po_props = {
            "cabinet_count": self.warehouse.cabinet_count,
            "cabinet_orientation": self.warehouse.cabinet_orientation,
            "weight_unit": self.warehouse.weight_unit,
            "cabinet_size": self.warehouse.cabinet_size,
            "updated_datetime": datetime.utcnow()
        }

        update_dict = self.split_props(po_props)

        #if self._operations:
        #    update_dict["$push"] = {
        #        "operation_records": {"$each": [o.to_mongo() for o in self._operations]}
        #    }

        if update_dict:
            self.warehouse.update_one(update_dict, session=transaction_session)
