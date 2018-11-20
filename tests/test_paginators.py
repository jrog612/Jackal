from rest_framework import serializers

from jackal.paginators import JackalPaginator
from jackal.settings import jackal_settings
from jackal.tests import JackalTestCase
from tests.models import TestModel


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ('field_int',)


class TestPaginator(JackalTestCase):
    def setUp(self):
        obj_list = [TestModel(field_int=i) for i in range(1, 15)]
        TestModel.objects.bulk_create(obj_list)
        self.queryset = TestModel.objects.order_by('id')
        self.page_length = jackal_settings.PAGE_LENGTH

    def test_paginator(self):
        paginator = JackalPaginator(self.queryset, 1)
        response_data = paginator.response_data()

        self.assertEqual(response_data['current_page'], 1)
        self.assertEqual(response_data['total_page'], self.queryset.count() // self.page_length + 1)
        self.assertEqual(response_data['page_length'], self.page_length)
        self.assertEqual(response_data['count'], self.queryset.count())

        self.assertLen(jackal_settings.PAGE_LENGTH, response_data['data'])
        self.assertEqual(self.queryset.first(), response_data['data'][0])

        response_data = JackalPaginator(self.queryset, 2).response_data()

        self.assertEqual(response_data['current_page'], 2)
        self.assertLen(TestModel.objects.all()[self.page_length:].count(), response_data['data'])

        response_data = JackalPaginator(self.queryset, 1, 20).response_data()

        self.assertLen(TestModel.objects.count(), response_data['data'])

    def test_paginator_serialized(self):
        paginator = JackalPaginator(self.queryset, 1)
        response_data = paginator.serialized_data(TestSerializer)

        self.assertEqual(response_data['current_page'], 1)
        self.assertEqual(response_data['total_page'], self.queryset.count() // self.page_length + 1)
        self.assertEqual(response_data['page_length'], self.page_length)
        self.assertEqual(response_data['count'], self.queryset.count())

        self.assertEqual(response_data['data'], TestSerializer(self.queryset[:self.page_length], many=True).data)
