class JackalBaseStructure:
    prefix = 'structure'

    @classmethod
    def get_structure(cls):
        """
        정의된 prefix 값을 이용하여 해당 클래스 내의 {prefix}_ 형태로 시작하는 모든 항목들을 가져옵니다.
        만약 항목이 함수라면, 해당 함수를 실행한 값을 최종 딕셔너리에 업데이트하고, 일반 딕셔너리라면 바로 업데이트합니다.
        사전도, 함수도 아니라면 건너 뜁니다.
        """
        ret_dict = {}
        for key in cls.__dict__.keys():
            if key.find('{}_'.format(cls.prefix)) == 0:
                value = getattr(cls, key, {})
                if callable(value):
                    ret_dict.update(value())
                elif type(value) is dict:
                    ret_dict.update(value)
                else:
                    continue

        return ret_dict


class BaseStatusCondition(JackalBaseStructure):
    pass


class BaseStatusReadable(JackalBaseStructure):
    pass


class BaseQueryFunction:
    prefix = 'func'

    @classmethod
    def get_function_set(cls):
        ret_dict = {}

        for name, func in cls.__dict__.items():
            if name.find('{}_'.format(cls.prefix)) == 0:
                name = name.replace('{}_'.format(cls.prefix), '')
                ret_dict[name] = func.__func__
        return ret_dict


class DefaultQueryFunction(BaseQueryFunction):
    @staticmethod
    def func_to_list(data):
        return data.split(',')

    @staticmethod
    def func_to_boolean(data):
        return data.lower() == 'true'
