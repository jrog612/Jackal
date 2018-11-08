from jackal.consts import none_values
from jackal.exceptions import FieldException


class remove:
    pass


class BaseInspector:
    """
    example of inspector map

    {
        'age': {
            'type_change': int,
            'if_null': 18,
            'required': true,
            'validator': ValidatorClass,
        },
    }

    """

    def __init__(self, target_dict, inspect_map):
        self.target = target_dict
        self.map = inspect_map
        self._inspected_data = target_dict

    def get_required_fields(self):
        return [key for key, value in self.map.items() if value.get('required', False)]

    def get_expected_fields(self):
        return self.map.keys()

    def get_type_change_fields(self):
        return {
            key: value.get('type_change') for key, value in self.map.items() if
            value.get('type_change') is not None
        }

    def get_validate_fields(self):
        return {
            key: value.get('validator') for key, value in self.map.items() if
            value.get('validator') is not None
        }

    def get_if_null_fields(self):
        return {
            key: value.get('validator') for key, value in self.map.items() if
            value.get('validator') is not None
        }

    def get_field(self, key, default=None):
        return self.map.get(key, default)

    def expected(self, data):
        fields = self.get_required_fields()
        expected_dict = {key: value for key, value in data.items() if key in fields}
        return expected_dict

    def required(self, data):
        fields = self.get_required_fields()
        for req in fields:
            if data.get(req) in none_values:
                raise FieldException(field=req, message='Required')
        return True

    def convert_type(self, data):
        fields = self.get_type_change_fields()
        ret_dict = {}
        for key, chn in fields.items():
            val = data.get(key)
            if val in none_values:
                continue
            ret_dict[key] = chn(val)
        return ret_dict

    def check_validate(self, data):
        fields = self.get_validate_fields()
        for key, validator in fields.items():
            v = validator(data.get(key))
            if not v.is_valid():
                raise FieldException(field=key, message='Invalid Value', context={'value': data.get(key)})
        return True

    def convert_if_null(self, data):
        fields = self.get_if_null_fields()
        ret_data = dict()
        for key, value in fields.items():
            v = value
            if data.get(key) not in none_values:
                v = data[key]
            elif v is remove:
                continue
            ret_data[key] = v

        return ret_data

    @property
    def inspected_data(self):
        self._inspected_data = self.expected(self._inspected_data)
        self.required(self._inspected_data)
        self._inspected_data = self.convert_type(self._inspected_data)
        self.check_validate(self._inspected_data)
        self._inspected_data = self.convert_if_null(self._inspected_data)

        return self._inspected_data


class BaseValidator:
    valid_map = {}

    def __init__(self, value):
        self.value = value

    def is_valid(self):
        return True
