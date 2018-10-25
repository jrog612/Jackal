from django.test import TestCase

from jackal import inspectors


class MyTestInspector(inspectors.Inspector):
    integer_field = inspectors.IntegerField()
    string_field = inspectors.StringField()
    boolean_field = inspectors.BooleanField()
    required_field = inspectors.IntegerField(required=True)


class TestInspector(TestCase):
    def setUp(self):
        self.pre_inspect = {
            'integer_field': 15,
            'string_field': 'string',
            'boolean_field': False,
            'unexpected_field': 'uep',
            'required_field': 'required'
        }

    def test_inspector_append(self):
        pass