from jackal.decorators import return_mutable
from jackal.settings import jackal_settings


@return_mutable('dict')
def structure_loader(ret_data, key='VALID_STRUCTURE'):
    for structure_class in getattr(jackal_settings, key):
        ret_data.update(structure_class.get_structure())


@return_mutable('dict')
def query_function_loader(ret_data):
    for cls in jackal_settings.QUERY_FUNCTION_CLASSES:
        ret_data.update(cls.get_function_set())
