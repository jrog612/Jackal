from django.test import TestCase

from jackal.settings import JackalSettings


class TestStructure(TestCase):
    def test_structure_import_in_settings(self):
        settings = JackalSettings({
            'STATUS_CONDITION_CLASSES': [
                'tests.test_structures.MyTestStructure'
            ]
        })

        assert hasattr(settings.STATUS_CONDITION_CLASSES[0], 'prefix')
        assert hasattr(settings.STATUS_CONDITION_CLASSES[0], 'stru_test')
