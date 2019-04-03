from django.db import models

from jackal.models import JackalModel
from jackal.tests import JackalTransactionTestCase


class TestModelA(JackalModel):
    field_a = models.CharField(max_length=10, null=True)


class TestModelB(JackalModel):
    model_a = models.ForeignKey(TestModelA, on_delete=models.CASCADE, null=True)


class TestModelC(JackalModel):
    model_bs = models.ManyToManyField(TestModelB)


class SoftDeleteTest(JackalTransactionTestCase):
    def test_soft_delete(self):
        TestModelA.objects.create(field_a='a')
        TestModelA.objects.create(field_a='b')
        soft_delete = TestModelA.objects.create(field_a='c')
        real_delete = TestModelA.objects.create(field_a='d')

        soft_delete.delete()
        self.assertIsNotNone(soft_delete.deleted_at)
        self.assertLen(3, TestModelA.objects.all())
        self.assertLen(4, TestModelA.defaults.all())

        real_delete.delete(soft=False)
        self.assertLen(2, TestModelA.objects.all())
        self.assertLen(3, TestModelA.defaults.all())

        TestModelA.objects.all().delete()
        self.assertLen(0, TestModelA.objects.all())
        self.assertLen(3, TestModelA.defaults.all())

    def test_relation_soft_delete(self):
        a = TestModelA.objects.create(field_a='a')
        b1 = TestModelB.objects.create(model_a=a)
        b2 = TestModelB.objects.create(model_a=a)
        b3 = TestModelB.objects.create(model_a=a)
        c = TestModelC.objects.create()
        c.model_bs.add(b1, b2, b3)

        b1.delete()
        self.assertLen(2, a.testmodelb_set.all())
        self.assertLen(2, c.model_bs.all())

        self.assertLen(3, a.testmodelb_set(manager='defaults').all())
        self.assertLen(3, c.model_bs.defaults.all())
