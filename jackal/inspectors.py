from jackal.exceptions import FieldException
from jackal.settings import jackal_settings


class remove:
    """
    When if_null is this class, that will removed in value dict.
    """
    pass


class _Getter:
    def get_required_fields(self):
        return [key for key, value in self.map.items() if value.get('required', False)]

    def get_expected_fields(self):
        return self.map.keys()

    def get_type_change_fields(self):
        return {
            key: value.get('type_to') for key, value in self.map.items() if
            value.get('type_to') is not None
        }

    def get_validate_fields(self):
        return {
            key: value.get('validator') for key, value in self.map.items() if
            value.get('validator') is not None
        }

    def get_if_null_fields(self):
        return {
            key: value.get('if_null') for key, value in self.map.items() if
            value.get('if_null') is not None
        }

    def get_none_values(self):
        return self.none_values if self.none_values is not None else jackal_settings.DEFAULT_NONE_VALUES


class Inspector(_Getter):
    none_values = None
    required_exception_class = FieldException
    required_message = 'value is required'

    """
    example of inspector map

    {
        'age': {
            'type_to': int,
            'if_null': 18,
            'required': true,
            'validator': ValidatorClass,
        },
    }
    """

    def __init__(self, target_dict, inspect_map):
        self.target = target_dict
        self.map = inspect_map

    def expected(self, data):
        """
        Remove unexpected values.
        """
        fields = self.get_expected_fields()
        expected_dict = {key: value for key, value in data.items() if key in fields}
        return expected_dict

    def required(self, data):
        """
        Check required values are not contained or null
        """
        fields = self.get_required_fields()
        for req in fields:
            if data.get(req) in self.get_none_values():
                raise self.required_exception_class(field=req, message=self.required_message)
        return True

    def convert_type(self, data):
        """
        Convert type to given function
        """
        fields = self.get_type_change_fields()
        ret_dict = dict()

        for key, value in data.items():
            if key in fields and value not in self.get_none_values():
                ret_dict[key] = fields[key](value)
                continue

            ret_dict[key] = value

        return ret_dict

    def check_validate(self, data):
        """
        Run given validater's is_valid function.
        """
        fields = self.get_validate_fields()
        for key, validator in fields.items():
            v = validator(value=data.get(key), field_name=key, total_data=data, inspector=self)
            if not v.is_valid():
                raise v.exception_class(field=key, message=v.invalid_message, context={'value': data.get(key)})
        return True

    def convert_if_null(self, data):
        """
        If value is none, convert given value of run function.
        """
        fields = self.get_if_null_fields()
        ret_dict = dict()

        for key, value in data.items():
            if key not in fields or value not in self.get_none_values():
                # Case - When value is not in none values: Add dict by passed value.
                ret_dict[key] = value
                continue

            if fields[key] is remove:
                # Case - When if_null value is remove class: Remove this key in dict.
                continue

            # Case - value is not exists or contained none values: Add default value.
            default = fields[key]
            ret_dict[key] = default() if callable(default) else default

        return ret_dict

    @property
    def inspected_data(self):
        ins_data = self.target
        # 1. Remove unexpected data.
        ins_data = self.expected(ins_data)
        # 2. Check required fields.
        self.required(ins_data)
        # 3. Convert type.
        ins_data = self.convert_type(ins_data)
        # 4. Check validation of value.
        self.check_validate(ins_data)
        # 5. Convert if data is null or not exists.
        ins_data = self.convert_if_null(ins_data)
        return ins_data


class BaseValidator:
    """
    You can customize this validator. Please override is_valid function.
    """
    default_invalid_message = 'Invalid Value'
    exception_class = FieldException

    def __init__(self, value, field_name, **kwargs):
        self.value = value
        self.field_name = field_name
        self.kwargs = kwargs
        self.invalid_message = self.default_invalid_message

    def is_valid(self):
        return True
