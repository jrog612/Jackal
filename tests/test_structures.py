from django.test import TestCase

from jackal.settings import JackalSettings
from jackal.structures import JackalBaseStructure


class MyTestStructure(JackalBaseStructure):
    prefix = 'stru'

    def stru__test(self):
        return {
            'test': 'test',
        }


class TestStructure(TestCase):
    def test_structure_import_in_settings(self):
        settings = JackalSettings({
            'STATUS_CONDITION_CLASSES': [
                'tests.test_structures.MyTestStructure'
            ]
        })

        assert settings.STATUS_CONDITION_CLASSES[0] is MyTestStructure
