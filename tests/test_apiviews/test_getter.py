from rest_framework.test import APITestCase

from jackal.views.base import JackalAPIView

test_filter_map = {
    'a': 'b'
}

test_lookup_map = {
    'c': 'd'
}

test_extra_kwargs = {
    'e': 'f'
}


class GetterTestAPIView(JackalAPIView):
    filter_map = test_filter_map
    extra_kwargs = test_extra_kwargs
    lookup_map = test_lookup_map

    def post(self, request):
        append_dict = request.data.dict()
        return self.simple_response({
            'extra_kwargs': self.get_extra_kwargs(request, **append_dict),
            'lookup_map': self.get_lookup_map(request, **append_dict),
            'filter_map': self.get_filter_map(request, **append_dict),
        })


class APIViewTest(APITestCase):
    def test_api_view_dict(self):
        append_dict = {'g': 'h'}
        extra_kwargs = {**test_extra_kwargs, **append_dict}
        lookup_map = {**test_lookup_map, **append_dict}
        filter_map = {**test_filter_map, **append_dict}

        response = self.client.post('/getter', append_dict)
        result = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(result.get('extra_kwargs'), extra_kwargs,)
        self.assertEqual(result.get('lookup_map'), lookup_map,)
        self.assertEqual(result.get('filter_map'), filter_map,)

