from django.test import TestCase

from jackal.exceptions import FieldException
from jackal.inspectors import Inspector, remove


class TestInspector(TestCase):
    def setUp(self):
        self.pre_inspect = {
            'integer_field': 15,
            'string_field': 'string',
            'boolean_field': False,
            'unexpected_field': 'uep',
            'required_field': 'required'
        }

    def test_expected(self):
        pre_inspect = {
            'a': 'a',
            'b': 'a',
            'c': 'a',
            'd': 'a',
        }
        inspect_map = {
            'a': {},
            'b': {},
            'd': {}
        }
        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data

        self.assertEqual({'a': 'a', 'b': 'a', 'd': 'a'}, result)
        self.assertNotIn('c', result)

    def test_required(self):
        pre_inspect = {
            'a': 'a',
            'c': 'a',
            'd': 'a',
        }
        inspect_map = {
            'a': {},
            'b': {'required': True},
            'd': {}
        }

        with self.assertRaises(FieldException) as res:
            ins = Inspector(pre_inspect, inspect_map)
            ins.inspected_data
        self.assertEqual('b', res.exception.field)

        pre_inspect.update({'b': 'a'})

        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data
        self.assertEqual({'a': 'a', 'b': 'a', 'd': 'a'}, result)

    def test_convert(self):
        pre_inspect = {
            'a': 121,
            'b': '1234',
        }
        inspect_map = {
            'a': {'type_to': str},
            'b': {'type_to': int},
        }

        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data
        self.assertEqual({'a': '121', 'b': 1234}, result)

    def test_if_null(self):
        pre_inspect = {
            'a': '',
            'b': None,
            'c': {},
            'd': []
        }
        inspect_map = {
            'a': {'if_null': remove},
            'b': {'if_null': None},
            'c': {'if_null': 'default'},
            'd': {'if_null': 100},

        }

        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data
        self.assertEqual({
            'b': None, 'c': 'default', 'd': 100
        }, result)
