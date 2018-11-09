import random

from django.db.models import Q

from jackal.exceptions import NotFound
from jackal.filters import JackalQueryFilter
from jackal.tests import JackalTransactionTestCase
from tests.models import TestModel


class TestQueryFilter(JackalTransactionTestCase):
    def setUp(self):
        self.max_length = 10
        self.objs = [TestModel(
            field_int=i, field_char=random.choice(['A Char', 'B Char', 'C Char']),
            field_text=random.choice(['A Char', 'B Char', 'C Char']),
        ) for i in range(1, self.max_length + 1)]
        TestModel.objects.bulk_create(self.objs)
        self.filter_map = {
            'int_gte': 'field_int__gte',
            'int_lte': 'field_int__lte',
            'field_char': 'field_char__contains',
            'field_text': 'field_text__contains',
            'field_a': 'field_a',
            'field_b': 'field_b'
        }
        self.search_dict = {
            'all': ('field_char__contains', 'field_text__contains', 'field_int__contains'),
            'field_char': 'field_char__contains',
            'field_text': 'field_text__contains',
            'field_int': 'field_int__contains',
        }

    def assertEqualQuerySet(self, set1, set2):
        listed_1 = list(set1.order_by('id').values_list('id', flat=True))
        listed_2 = list(set2.order_by('id').values_list('id', flat=True))
        self.assertEqual(listed_1, listed_2)

    def test_filter_map(self):
        f = JackalQueryFilter(TestModel.objects.all(), {})
        queryset = f.filter_map(self.filter_map).queryset
        self.assertEqualQuerySet(TestModel.objects.filter(), queryset)

        params = {'int_gte': 5}
        f = JackalQueryFilter(TestModel.objects.all(), params)
        queryset = f.filter_map(self.filter_map).queryset
        self.assertEqualQuerySet(TestModel.objects.filter(field_int__gte=5), queryset)

        params.update({'field_char': 'A Char'})
        f = JackalQueryFilter(TestModel.objects.all(), params)
        queryset = f.filter_map(self.filter_map).queryset
        self.assertEqualQuerySet(TestModel.objects.filter(field_int__gte=5, field_char__contains='A Char'), queryset)

    def test_search(self):
        f = JackalQueryFilter(TestModel.objects.all(), {})
        queryset = f.search(self.search_dict).queryset
        self.assertEqualQuerySet(TestModel.objects.all(), queryset)

        params = {'search_keyword': 'A Text'}
        f = JackalQueryFilter(TestModel.objects.all(), params)
        queryset = f.search(self.search_dict).queryset
        self.assertEqualQuerySet(TestModel.objects.filter(
            Q(field_char__contains='A Text') |
            Q(field_text__contains='A Text') |
            Q(field_int__contains='A Text')
        ), queryset)

        params = {'search_keyword': 'A Text', 'search_type': 'field_char'}
        f = JackalQueryFilter(TestModel.objects.all(), params)
        queryset = f.search(self.search_dict).queryset
        self.assertEqualQuerySet(TestModel.objects.filter(field_char__contains='A Text'), queryset)

    def test_get(self):
        f = JackalQueryFilter(TestModel.objects.all())
        with self.assertRaises(NotFound):
            f.get(True, field_a=1)

        obj = f.get(field_int=1)
        self.assertIsInstance(obj, TestModel)
        self.assertEqual(obj.field_int, 1)

    def test_extra(self):
        f = JackalQueryFilter(TestModel.objects.all())
        queryset = f.extra(field_int__gte=5).queryset

        self.assertEqualQuerySet(TestModel.objects.filter(field_int__gte=5), queryset)

        for i, o in enumerate(TestModel.objects.all()):
            o.field_a = self.max_length - i
            o.save()

        f = JackalQueryFilter(TestModel.objects.all(), {'ordering': '-field_a'})
        queryset = f.ordering().queryset

        for i, o in enumerate(queryset):
            self.assertEqual(o.field_a, self.max_length - i)
