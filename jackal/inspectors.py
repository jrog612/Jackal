class _inspect_const:
    pass


class _empty(_inspect_const):
    pass


class _required(_inspect_const):
    def __init__(self, exc):
        self.exception = exc


class BaseInspector:
    _declare_fields = {}

    def __init__(self, data=None, many=False):
        self.initial_data = data
        self.is_many = many
        self.inspected_data = None
        self.prepare()

    def _set_declare_fields(self):
        for key, value in self.__dict__.items():
            if isinstance(value, BaseField):
                self._declare_fields[key] = value

    def prepare(self):
        self._set_declare_fields()

    def inspect(self):
        if self.is_many:
            self.inspected_data = []
            for d in self.initial_data:
                self.inspected_data.append(self._inspect(d))
        else:
            self.inspected_data = self._inspect(self.initial_data)
        return self.inspected_data

    def _inspect(self, data):
        ret_data = {}

        for field_name, field in self._declare_fields.items():
            inspect_value = field.inspect_value(data.get(field_name))

            if issubclass(inspect_value, _inspect_const):
                self._inspect_const_handle(inspect_value)
            else:
                ret_data[field_name] = inspect_value

        return ret_data

    def _inspect_const_handle(self, cls):
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
