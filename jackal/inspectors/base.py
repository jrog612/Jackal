from jackal.consts import iterator, none_values
from jackal.exceptions import ConvertError
from jackal.inspectors.consts import Empty, InspectConst, Required, TypeWrong
from jackal.consts import Unset


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


class BaseConverter:
    default_replacement = {}

    def __init__(self, convert_type, field, replacement=None):
        self.convert_type = convert_type
        self.field = field
        self.replacement = replacement if replacement is not None else self.default_replacement

    def error(self, message, value):
        return ConvertError(message=message, value=value, field_class=self.field.__class__, field_ins=self.field)

    def convert(self, value, hard=False):
        try:
            self.converting(value, hard)
        except Exception as e:
            if isinstance(e, ConvertError):
                raise e
            else:
                message = getattr(e, 'message', '{} error raised while jackal inspector convert type.'.format(e))
                raise self.error(message, value)

    def converting(self, value, hard=False):
        return self.convert_type(value)

    def replace(self, value):
        ret_value = value
        for key, value in self.replacement.items():
            ret_value = ret_value.replace(key, value)
        return ret_value


class BaseField:
    field_type = None
    default_converter = BaseConverter

    def __init__(self, required=False, check_type=False,
                 skip_convert=False, except_to_default=True,
                 hard=False, converter_class=None, replacement=None, **kwargs):
        self.initial_value = Unset
        self.inspected_value = Unset

        self.is_required = required
        self.is_check_type = check_type
        self.skip_convert = skip_convert
        self.hard = hard
        self.default_value = self.kwargs.pop('default', Empty)
        self.kwargs = kwargs
        self.replacement = replacement

        self.except_to_default = False if self.default_value is Empty else except_to_default
        self.converter_class = self.default_converter if converter_class is None else converter_class

    def get_converter(self):
        return self.converter_class(self.field_type, self, self.replacement)

    def get_default_value(self):
        if self.default_value is Empty:
            return Empty
        if callable(self.default_value):
            return self.default_value()
        else:
            return self.default_value

    def inspect_value(self, value):
        """
        1. check required.
        2. convert type.
        3. check type.
        4. set default
        """
        self.initial_value = value
        inspecting = value

        try:
            if not self.check_required(inspecting):
                return Required

            if not self.skip_convert:
                inspecting = self.converting(inspecting)

            if not self.check_type(inspecting):
                return TypeWrong

            self.inspected_value = inspecting
            return inspecting

        except Exception as e:
            if self.except_to_default:
                return self.get_default_value()
            else:
                raise e

    def converting(self, value):
        converter = self.get_converter()
        ret_value = value
        ret_value = converter.replace(ret_value)
        return converter.convert(ret_value, self.hard)

    def check_required(self, value):
        return not (self.is_required and value in none_values)

    def check_type(self, value):
        if self.is_check_type:
            if isinstance(self.field_type, iterator):
                return type(value) in self.field_type
            else:
                return type(value) is self.field_type
        return True
