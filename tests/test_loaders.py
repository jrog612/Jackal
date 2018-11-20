from django.test import override_settings

from jackal.loaders import query_function_loader, structure_loader
from jackal.settings import DEFAULT_QUERY_FUNCTION
from jackal.structures import BaseQueryFunction, DefaultQueryFunction, JackalBaseStructure
from jackal.tests import JackalTestCase

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


class TestLoader(JackalTestCase):
    def test_structure_loader(self):
        with override_settings(JACKAL={
            'STATUS_CONDITION_CLASSES': [
                'tests.test_loaders.MyTestStructure'
            ],
            'CUSTOM_STRUCTURES': {
                'my_structure': [
                    'tests.test_loaders.MyTestCustomStructure'
                ]
            }
        }):
            structures = structure_loader('STATUS_CONDITION_CLASSES')
            self.assertEqual(structures['test_key'], test_value)

            structures = structure_loader('my_structure')
            self.assertEqual(structures['set1'], test_value)

    def test_query_function_loader(self):
        with override_settings(JACKAL={
            'QUERY_FUNCTION_CLASSES': [
                'tests.test_loaders.MyQueryFunction',
                DEFAULT_QUERY_FUNCTION,
            ]
        }):
            funcs = query_function_loader()

            self.assertIn('to_boolean', funcs)
            self.assertIn('to_list', funcs)
            self.assertIn('test_func', funcs)
