from django.test import TestCase, override_settings

from jackal.loaders import structure_loader
from jackal.settings import JackalSettings
from jackal.structures import JackalBaseStructure

test_value = {
    'field_1': 'asdf',
    'field_2': 'asdf'
}


class MyTestStructure(JackalBaseStructure):
    prefix = 'stru'

    @classmethod
    def stru__test(cls):
        return {
            'test_key': test_value,
        }


class TestStructure(TestCase):
    def test_structure_import_in_settings(self):
        settings = JackalSettings({
            'STATUS_CONDITION_CLASSES': [
                'tests.test_structures.MyTestStructure'
            ]
        })

        assert hasattr(settings.STATUS_CONDITION_CLASSES[0], 'prefix')
        assert hasattr(settings.STATUS_CONDITION_CLASSES[0], 'stru__test')

    def test_structure_load(self):
        with override_settings(JACKAL={'STATUS_CONDITION_CLASSES': [
            'tests.test_structures.MyTestStructure'
        ]}):
            structures = structure_loader('STATUS_CONDITION_CLASSES')
            assert structures['test_key'] == test_value
