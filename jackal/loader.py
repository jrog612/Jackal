from jackal.settings import jackal_settings


def structure_loader(key='STABILIZING_STRUCTURES'):
    ret_dict = dict()
    for structure_class in getattr(jackal_settings, key):
        ret_dict.update(structure_class.get_structure())
    return ret_dict


