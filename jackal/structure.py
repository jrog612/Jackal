class JackalBaseStructure:
    pre_fix = 'structure'

    @classmethod
    def get_structure(cls):
        ret_dict = {}
        for key, value in cls.__dict__.items():
            if key.find('{}_'.format(cls.pre_fix)) == 0:
                ret_dict.update(value)
        return ret_dict

