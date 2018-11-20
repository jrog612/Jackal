from jackal.structures import BaseQueryFunction, JackalBaseStructure

test_value = {
    'field_1': 'asdf',
    'field_2': 'asdf'
}


class MyTestStructure(JackalBaseStructure):
    prefix = 'stru'

    @classmethod
    def stru_test(cls):
        return {
            'test_key': test_value,
        }


class MyTestCustomStructure(JackalBaseStructure):
    prefix = 'stru'

    @classmethod
    def stru_test(cls):
        return {
            'set1': test_value,
        }


class MyQueryFunction(BaseQueryFunction):
    @staticmethod
    def func_test_func(data):
        return True
