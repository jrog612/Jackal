from jackal.decorators import return_mutable
from jackal.settings import jackal_settings
from jackal.structure import JackalBaseStructure, QueryFunction


@return_mutable('dict')
def structure_loader(ret_data, key='VALID_STRUCTURE'):
    for cls in getattr(jackal_settings, key):
        if isinstance(cls, JackalBaseStructure):
            ret_data.update(cls.get_structure())


@return_mutable('dict')
def query_function_loader(ret_data):
    for cls in jackal_settings.QUERY_FUNCTION_CLASSES:
        if isinstance(cls, QueryFunction):
            ret_data.update(cls.get_function_set())
