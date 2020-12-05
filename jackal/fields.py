import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import TextField


def dumps(value):
    return json.dumps(
        value,
        cls=DjangoJSONEncoder,
        sort_keys=True,
        indent=2,
        separators=(',', ': ')
    )


class JSONField(TextField):
    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer', dumps)
        self.deserializer = kwargs.pop('deserializer', json.loads)
        super(JSONField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        kwargs['serializer'] = self.serializer
        kwargs['deserializer'] = self.deserializer
        return name, path, args, kwargs

    def to_python(self, value):
        if value == "":
            return None
        try:
            if isinstance(value, str):
                return self.deserializer(value)
            elif isinstance(value, bytes):
                return self.deserializer(value.decode('utf8'))
        except ValueError:
            pass
        return value

    def get_prep_value(self, value):
        if value == "":
            return None
        if isinstance(value, (dict, list)):
            return self.serializer(value)
        return super(JSONField, self).get_prep_value(value)

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def get_default(self):
        if self.has_default():
            return self.default() if callable(self.default) else self.default
        return ""

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, (dict, list)):
            return self.serializer(value)
        else:
            return super(JSONField,
                         self).get_db_prep_save(value, *args, **kwargs)

    def value_from_object(self, obj):
        value = super(JSONField, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return self.serializer(value)
