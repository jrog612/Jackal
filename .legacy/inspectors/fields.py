from jackal.inspectors.base import BaseField
from jackal.converters import BooleanConverter, IntegerConverter

__all__ = [
    'BooleanField', 'StringField', 'IntegerField', 'FloatField',
    # 'EmailField', 'CallNumberField',
]


class StringField(BaseField):
    field_type = str


class IntegerField(BaseField):
    field_type = int
    default_converter = IntegerConverter


class FloatField(BaseField):
    field_type = float


class BooleanField(BaseField):
    field_type = bool
    default_converter = BooleanConverter

# class EmailField(BaseField):
#     field_type = str

# class CallNumberField(BaseField):
#     field_type = str

# class DictionaryField(BaseField):
#     field_type = dict
#     allow_type = (str, bool, int)


# class ArrayField(BaseField):
#     field_type = list
#     allow_type = (str, bool, int)
