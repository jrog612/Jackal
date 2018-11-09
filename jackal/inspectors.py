from jackal.consts import none_values
from jackal.exceptions import FieldException


class remove:
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

    # def get_validate_fields(self):
    #     return {
    #         key: value.get('validator') for key, value in self.map.items() if
    #         value.get('validator') is not None
    #     }

    def get_if_null_fields(self):
        return {
            key: value.get('if_null') for key, value in self.map.items() if
            value.get('if_null') is not None
        }

    def get_field(self, key, default=None):
        return self.map.get(key, default)


class BaseInspector(_Getter):
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
        fields = self.get_expected_fields()
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
        ret_dict = dict()

        for key, value in data.items():
            if key in fields and value not in none_values:
                ret_dict[key] = fields[key](value)
                continue

            ret_dict[key] = value

        return ret_dict

    # def check_validate(self, data):
    #     fields = self.get_validate_fields()
    #     for key, validator in fields.items():
    #         v = validator(data.get(key))
    #         if not v.is_valid():
    #             raise FieldException(field=key, message='Invalid Value', context={'value': data.get(key)})
    #     return True

    def convert_if_null(self, data):
        fields = self.get_if_null_fields()
        ret_dict = dict()

        for key, value in data.items():
            if key not in fields or value not in none_values:
                ret_dict[key] = value
                continue

            if fields[key] is remove:
                continue

            default = fields[key]
            ret_dict[key] = default() if callable(default) else default

        return ret_dict

    @property
    def inspected_data(self):
        ins_data = self.target
        ins_data = self.expected(ins_data)
        self.required(ins_data)
        ins_data = self.convert_type(ins_data)

        # self.check_validate(ins_data)

        ins_data = self.convert_if_null(ins_data)
        return ins_data

# class BaseValidator:
#     valid_map = {}
#
#     def __init__(self, value):
#         self.value = value
#
#     def is_valid(self):
#         return True
