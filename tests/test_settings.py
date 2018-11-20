from django.test import TestCase, override_settings

from jackal.settings import JackalSettings, jackal_settings
from jackal.structures import DefaultQueryFunction


class TestSettings(TestCase):
    def test_import_error(self):
        settings = JackalSettings({
            'STATUS_CONDITION_CLASSES': [
                'tests.invalid.InvalidStructureClass'
            ]
        })
        with self.assertRaises(ImportError):
            print(settings.STATUS_CONDITION_CLASSES)

    def test_override_settings(self):
        assert jackal_settings.PAGE_LENGTH is 10

        with override_settings(JACKAL={'PAGE_LENGTH': 20}):
            assert jackal_settings.PAGE_LENGTH == 20

        assert jackal_settings.PAGE_LENGTH is 10

    def test_str_import(self):
        dq = jackal_settings.QUERY_FUNCTION_CLASSES[0]
        assert dq is DefaultQueryFunction
