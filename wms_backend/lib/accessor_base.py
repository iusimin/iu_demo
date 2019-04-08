
from wms_backend.model.mongo.operation_record import CPOperationRecord

class AccessorBase(object):
    def __init__(self, *args, **kwargs):
        self._operations = []

    def split_props(self, props):
        set_prop = {k:v for k, v in props.iteritems() if v is not None}
        upset_prop = {k:True for k, v in props.iteritems() if v is None}
        update_dict = {}
        if set_prop:
            update_dict["$set"] = set_prop
        if upset_prop:
            update_dict["$unset"] = upset_prop
        return update_dict

    def add_operation(self, operator, operation, operation_description, operation_info, operation_datetime):
        self._operations.append(
            CPOperationRecord(
                operator=operator,
                operation=operation,
                operation_description=operation_description,
                operation_info=operation_info,
                operation_datetime=operation_datetime
            )
        )
