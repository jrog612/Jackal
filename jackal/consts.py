import collections

none_values = [[], {}, '', 'null', None, 'undefined']

iterator = collections.abc.Iterator


class Unset:
    pass


class ROUND_UP:
    pass


class ROUND_DOWN:
    pass


class ROUND_HALF:
    pass