class InspectConst:
    is_fail = False

    def __init__(self, pre_value, field_name, field, *args, **kwargs):
        self.pre_value = pre_value
        self.field_name = field_name
        self.field = field
        self.args = args
        self.kwargs = kwargs

    def handle(self):
        pass


class Unset(InspectConst):
    pass


class Empty(InspectConst):
    pass


class Required(InspectConst):
    is_fail = True

    def handle(self):
        pass


class TypeWrong(InspectConst):
    is_fail = True

    def handle(self):
        pass
