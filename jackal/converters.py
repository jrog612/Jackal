from jackal.inspectors.base import BaseConverter


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
