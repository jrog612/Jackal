from jackal.inspectors.base import BaseField


class BooleanField(BaseField):
    field_type = bool
    allow_type = (str, bool, int)


class StringField(BaseField):
    field_type = str
    allow_type = '*'


class IntegerField(BaseField):
    field_type = int
    allow_type = (str, float, int)


class FloatField(BaseField):
    field_type = float
    allow_type = (str, bool, int)


class NumberField(BaseField):
    field_type = (int, float)
    allow_type = (str, bool, int)


class EmailField(BaseField):
    field_type = str
    allow_type = (str, bool, int)


class CallNumberField(BaseField):
    field_type = str
    allow_type = (str, bool, int)

# class DictionaryField(BaseField):
#     field_type = dict
#     allow_type = (str, bool, int)
#
#
# class ArrayField(BaseField):
#     field_type = (tuple, set, list)
#     allow_type = (str, bool, int)
#
