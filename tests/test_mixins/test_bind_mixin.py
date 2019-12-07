from django.db import models

from jackal.fields import JSONField
from jackal.mixins.bind_mixin import BindMixin
from jackal.tests import JackalTransactionTestCase


class TestBindModel(BindMixin, models.Model):
    bound_fields = ['b_field1', 'b_field2']
    extra = JSONField(default=dict)
    field_char = models.CharField(max_length=150, null=True)


class TestBindModel2(BindMixin, models.Model):
    bind_field_name = 'b_field'
    bound_fields = ['b_field1', 'b_field2']
    b_field = JSONField(default=dict)


class SoftDeleteTest(JackalTransactionTestCase):
    def test_bind_values(self):
        tobj = TestBindModel()
        tobj.b_field1 = 'test_b_field1'
        tobj.field_char = 'char_field'
        tobj.save()
        tobj = TestBindModel.objects.get(id=tobj.id)
        self.assertEqual(tobj.b_field1, 'test_b_field1')
        self.assertEqual(tobj.extra, {'b_field1': 'test_b_field1'})
        self.assertIsNone(tobj.b_field2)
        self.assertEqual(tobj.field_char, 'char_field')
        with self.assertRaises(AttributeError):
            tobj.b_field3

    def test_different_bind_field_name(self):
        tobj = TestBindModel2()
        tobj.b_field1 = 'test_b_field1'
        tobj.save()
        tobj = TestBindModel2.objects.get(id=tobj.id)
        self.assertEqual(tobj.b_field1, 'test_b_field1')
        self.assertEqual(tobj.b_field, {'b_field1': 'test_b_field1'})
        self.assertIsNone(tobj.b_field2)
        with self.assertRaises(AttributeError):
            tobj.b_field3

    def test_create(self):
        tobj = TestBindModel.objects.create(
            b_field1='test_b_field1', field_char='char_field'
        )
        self.assertEqual(tobj.extra, {'b_field1': 'test_b_field1'})
        self.assertEqual(tobj.field_char, 'char_field')
