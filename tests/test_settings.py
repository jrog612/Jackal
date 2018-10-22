from django.test import TestCase, override_settings

from jackal.settings import JackalSettings, jackal_settings


class TestSettings(TestCase):
    def test_import_error(self):
        settings = JackalSettings({
            'INSPECT_STRUCTURE_CLASSES': [
                'tests.invalid.InvalidStructureClass'
            ]
        })
        with self.assertRaises(ImportError):
            print(settings.INSPECT_STRUCTURE_CLASSES)

    def test_override_settings(self):
        assert jackal_settings.PAGE_LENGTH is None

        with override_settings(JACKAL={'PAGE_LENGTH': 10}):
            assert jackal_settings.PAGE_LENGTH == 10

        assert jackal_settings.PAGE_LENGTH is None

