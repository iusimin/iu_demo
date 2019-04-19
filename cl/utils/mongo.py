from datetime import date, datetime

from bson import ObjectId


class MongoMixin(object):
    @classmethod
    def all_fields(cls):
        return cls._fields.keys()

    def dict_include(self):
        return self.all_fields()

    def dict_exclude(self):
        return []

    def to_dict_default(self, date_format="%Y-%m-%d"):
       def transform_field(value):
           if type(value) is ObjectId:
               return str(value)
           elif type(value) is list:
               return map(transform_field, value)
           elif issubclass(value.__class__, MongoMixin):
               if hasattr(value, 'to_dict'):
                   return value.to_dict()
               else:
                   return value.to_dict_default()
           elif type(value) is dict:
               return dict([(key, transform_field(val))
                   for key, val in value.iteritems()])
           elif type(value) is datetime or type(value) is date:
               return value.strftime(date_format)
           else:
               return value
       _dict = {}
       exclude = self.dict_exclude()
       for fname in self.dict_include():
           if fname not in exclude:
               value = getattr(self, fname)
               _dict[fname] = transform_field(value)
       return _dict
