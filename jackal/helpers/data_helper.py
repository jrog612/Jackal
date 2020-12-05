import collections


class JackalDictMapper:
    @staticmethod
    def av2bv(a_dict, b_dict):
        return {a_value: b_dict.get(a_key) for a_key, a_value in a_dict.items()}


def isiter(arg):
    return isinstance(arg, collections.Iterable) and not isinstance(arg, str)
