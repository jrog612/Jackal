from jackal.tests import JackalAPITestCase
from jackal.views.base import JackalAPIView
from tests.models import TestModel, TestSerializer


class FilteringTestAPI(JackalAPIView):
    model = TestModel
    queryset = TestModel.objects.all()
    filter_map = {
        'field_char': 'field_char__contains'
    }
    extra_kwargs = {
        'field_int': 1
    }

    def get(self, request):
        kind = request.query_params['kind']
        if kind == 'queryset':
            queryset = self.get_filtered_queryset(request)
            ser = TestSerializer(queryset, many=True)
        else:
            obj = self.get_object(request)
            ser = TestSerializer(obj)
        return self.simple_response(ser.data)


class TestAPIViewFiltering(JackalAPITestCase):
    def test_get_object(self):
        response = self.client.get('/filtering', {'kind': 'object'})
        self.assertStatusCode(404, response)

        obj = TestModel.objects.create(field_int=1)
        TestModel.objects.create(field_int=2)
        TestModel.objects.create(field_int=3)
        TestModel.objects.create(field_int=4)

        response = self.client.get('/filtering', {'kind': 'object'})
        result = response.json()
        self.assertSuccess(response)
        self.assertEqual(result['field_int'], obj.field_int)
        self.assertEqual(result['id'], obj.id)

    def test_get_filtered_queryset(self):
        obj1 = TestModel.objects.create(field_int=1, field_char='char')
        obj2 = TestModel.objects.create(field_int=1, field_char='chock')
        TestModel.objects.create(field_int=1, field_char='bb')
        TestModel.objects.create(field_int=2, field_char='ch')

        response = self.client.get('/filtering', {'kind': 'queryset', 'field_char': 'ch'})
        result = response.json()

        self.assertSuccess(response)
        self.assertLen(2, result)
        self.assertEqual(obj1.id, result[0]['id'])
        self.assertEqual(obj2.id, result[1]['id'])

        response = self.client.get('/filtering', {'kind': 'queryset', 'field_char': 'char'})
        result = response.json()

        self.assertSuccess(response)
        self.assertLen(1, result)
        self.assertEqual(obj1.id, result[0]['id'])
