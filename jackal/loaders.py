from jackal.settings import jackal_settings
from jackal.structures import JackalBaseStructure, BaseQueryFunction


def structure_loader(key):
    ret_data = dict()
    stru = getattr(jackal_settings, key, None)

    if stru is None:
        stru = jackal_settings.CUSTOM_STRUCTURES.get(key)

        if stru is None:
            return {}

    for cls in stru:
        if issubclass(cls, JackalBaseStructure):
            ret_data.update(cls.get_structure())
        else:
            continue
    return ret_data


def query_function_loader():
    ret_data = dict()
    for cls in jackal_settings.QUERY_FUNCTION_CLASSES:
        if issubclass(cls, BaseQueryFunction):
            ret_data.update(cls.get_function_set())

    return ret_data
