from jackal.exceptions import ConvertError


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
                message = getattr(e, 'message', '{} error raised while jackal inspector converting type.'.format(e))
                raise self.error(message, value)

    def converting(self, value, hard=False):
        return self.convert_type(value)

    def replace(self, value):
        ret_value = value
        for key, value in self.replacement.items():
            ret_value = ret_value.replace(key, value)
        return ret_value


class IntegerConverter(BaseConverter):
    pass
    # def convert_type(self, value):
    #     converting = value
    #
    #     if type(converting) is str:
    #         if self.hard and not converting.isdisit():
    #             raise self.convert_error('Invalid str to convert type', value)
    #
    #         converting = float(self._replace_value(converting))
    #
    #     if type(converting) is float:
    #         return self._round_value(converting)
    #
    #     if value is None:
    #         return value
    #
    #     return int(converting)
    #
    # def _replace_value(self, value):
    #     ret_value = value
    #     for key, value in self.replacement.items():
    #         ret_value = ret_value.replace(key, value)
    #     return ret_value
    #
    # def _round_value(self, value):
    #     if self.float_round is ROUND_UP:
    #         pass
    #     elif self.float_round is ROUND_HALF:
    #         pass
    #     elif self.float_round is ROUND_DOWN:
    #         return int(value)


class BooleanConverter(BaseConverter):
    def converting(self, value, hard=False):
        if not hard:
            return bool(value)

        elif type(value) in (int, bool):
            return bool(value)
        elif type(value) is str:
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            raise self.error('Invalid string to convert boolean', value)

        raise self.error('Invalid type to convert boolean', value)
