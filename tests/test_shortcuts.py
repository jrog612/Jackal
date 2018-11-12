from django.test import override_settings

from jackal.exceptions import NotFound
from jackal.settings import jackal_settings
from jackal.shortcuts import get_object_or_404, get_object_or_None, iterable, model_update, operating, status_checker, \
    status_readable
from jackal.structures import BaseStatusCondition, BaseStatusReadable
from jackal.tests import JackalTransactionTestCase
from tests.models import TestModel


class TestCondition(BaseStatusCondition):
    prefix = 'status'

    @classmethod
    def status__test(cls):
        return {
            'test': {
                2: (
                    ('<', 2), ('>', 0)
                )
            },
        }


class TestReadable(BaseStatusReadable):
    prefix = 'status'

    @classmethod
    def status__test(cls):
        return {
            'test': {
                1: 'one',
                2: 'two',
                0: 'zero'
            },
        }


class TestShortcuts(JackalTransactionTestCase):
    def test_iterable(self):
        self.assertTrue(iterable([1, 2, 3]))
        self.assertTrue(iterable((1, 2, 3)))
        self.assertTrue(iterable({1, 2, 3}))
        self.assertTrue(iterable({1: 1, 2: 2, 3: 3}))

        self.assertFalse(iterable('String Sentence'))
        self.assertFalse(iterable(None))
        self.assertFalse(iterable(False))
        self.assertFalse(iterable(True))
        self.assertFalse(iterable(123))

    def test_get_object_or(self):
        obj = TestModel.objects.create(field_int=1)

        self.assertIsNone(get_object_or_None(TestModel, field_int=2))
        self.assertEqual(get_object_or_None(TestModel, field_int=1), obj)

        with self.assertRaises(NotFound) as res:
            get_object_or_404(TestModel, field_int=2)

        self.assertIs(res.exception.model, TestModel)
        self.assertEqual(get_object_or_404(TestModel, field_int=1), obj)

    def test_model_update(self):
        obj = TestModel.objects.create(field_int=1, field_char='text')

        obj = model_update(obj, field_int=2, field_char='test2')

        self.assertEqual(obj.field_int, 2)
        self.assertEqual(obj.field_char, 'test2')

    def test_operating(self):
        self.assertTrue(operating(1, '==', 1))
        self.assertTrue(operating(1, '<=', 2))
        self.assertTrue(operating(1, '<', 2))
        self.assertTrue(operating(1, '>', 0))
        self.assertTrue(operating(1, '>=', 1))
        self.assertTrue(operating(1, '!=', 2))

        self.assertFalse(operating(1, '==', 2))
        self.assertFalse(operating(3, '<=', 2))
        self.assertFalse(operating(2, '<', 2))
        self.assertFalse(operating(1, '>', 1))
        self.assertFalse(operating(1, '>=', 2))
        self.assertFalse(operating(1, '!=', 1))

    def test_status_checker(self):
        with override_settings(JACKAL={
            'STATUS_CONDITION_CLASSES': [
                'tests.test_shortcuts.TestCondition'
            ]
        }):
            obj1 = TestModel.objects.create(field_int=1)
            obj0 = TestModel.objects.create(field_int=0)

            self.assertTrue(status_checker(2, obj1.field_int, 'test'))
            self.assertFalse(status_checker(2, obj0.field_int, 'test'))

    def test_readable_status(self):
        unknown = 'I do not know'
        with override_settings(JACKAL={
            'STATUS_READABLE_CLASSES': [
                'tests.test_shortcuts.TestReadable'
            ],
            'UNKNOWN_READABLE': unknown
        }):
            obj1 = TestModel.objects.create(field_int=1)
            obj0 = TestModel.objects.create(field_int=0)
            obj2 = TestModel.objects.create(field_int=2)

            self.assertEqual(status_readable(obj1.field_int, 'test'), 'one')
            self.assertEqual(status_readable(obj2.field_int, 'test'), 'two')
            self.assertEqual(status_readable(obj0.field_int, 'test'), 'zero')
            self.assertEqual(status_readable(4, 'test'), unknown)
