import collections

none_values = [[], {}, '', 'null', None, 'undefined']

iterator = collections.abc.Iterator


class Unset:
    pass
