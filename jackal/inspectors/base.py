from jackal.consts import iterator, none_values
from jackal.inspectors.consts import Empty, InspectConst, Required, TypeWrong, Unset


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
            pre_value = data.get(field_name)
            inspect_value = field.inspect_value(pre_value)

            if issubclass(inspect_value, InspectConst):
                self.inspect_const_handle(inspect_value, pre_value, field_name, field)
            else:
                ret_data[field_name] = inspect_value

        return ret_data

    def get_const_instance(self, const_class, pre_value, field_name, field):
        instance = const_class(pre_value, field_name, field)
        return instance

    def inspect_const_handle(self, const_class, pre_value, field_name, field):
        ins = self.get_const_instance(const_class, pre_value, field_name, field)
        result = ins.handle()
        return result


class BaseField:
    field_type = None

    def __init__(self, required=False, check_type=False, skip_convert=False, *args, **kwargs):
        self.is_required = required
        self.is_check_type = check_type
        self.skip_convert = skip_convert
        self.args = args
        self.default_value = self.kwargs.pop('default', Empty)
        self.kwargs = kwargs
        self.initial_value = Unset
        self.inspected_value = Unset

    @property
    def _default_value(self):
        if self.default_value is Empty:
            return Empty
        if callable(self.default_value):
            return self.default_value()
        else:
            return self.default_value

    def inspect_value(self, value):
        """
        1. check required.
        2. check type.
        3. convert type.
        4. set default
        """
        self.initial_value = value

        if not self.check_required(value):
            return Required
        if not self.check_type(value):
            return TypeWrong

        converted_value = self.convert_type(value)

        self.inspected_value = converted_value
        return converted_value

    def check_required(self, value):
        return not (self.is_required and value in none_values)

    def check_type(self, value):
        if self.is_check_type:
            if isinstance(self.field_type, iterator):
                return type(value) in self.field_type
            else:
                return type(value) is self.field_type
        return True

    def convert_type(self, value):
        if self.skip_convert:
            return value
        return None
