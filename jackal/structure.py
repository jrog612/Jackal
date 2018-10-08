class JackalBaseStructure:
    prefix = 'structure'

    @classmethod
    def get_structure(cls):
        ret_dict = {}
        for key, value in cls.__dict__.items():
            if key.find('{}_'.format(cls.prefix)) == 0:
                ret_dict.update(value)
        return ret_dict


class QueryFunction:
    prefix = 'func'

    @classmethod
    def get_function_set(cls):
        ret_dict = {}

        for name, func in cls.__dict__.items():
            if name.find('{}_'.format(cls.prefix)) == 0:
                name = name.replace('{}_'.format(cls.prefix))
                ret_dict[name] = func
        return ret_dict

    @staticmethod
    def func_to_list(data):
        return data.split(',')

    @staticmethod
    def func_to_boolean(data):
        return data.lower() == 'true'
