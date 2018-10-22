class BaseInspector:
    _declare_fields = {}

    def __init__(self, data=None, many=False):
        pass

    def inspect(self):
        pass


class BaseField:
    def __init__(self, required=False, default=None):
        pass

    def inspect_value(self, value):
        pass

    def convert_type(self):
        pass


class Inspector(BaseInspector):
    pass


class BooleanField(BaseField):
    pass


class StringField(BaseField):
    pass


class IntegerField(BaseField):
    pass


class NumberField(BaseField):
    pass


class FloatField(BaseField):
    pass


class EmailField(BaseField):
    pass


class CallNumberField(BaseField):
    pass


class DictionaryField(BaseField):
    pass


class ArrayField(BaseField):
    pass
