from jackal.exceptions import jackal_exception_handler
from jackal.tests import JackalAPITestCase
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

test_inspect_map = {
    'x': {}
}


class GetterResponseTestAPIView(JackalAPIView):
    filter_map = test_filter_map
    extra_kwargs = test_extra_kwargs
    lookup_map = test_lookup_map
    inspect_map = test_inspect_map

    def get(self, request):
        case = request.query_params.get('case')
        extra_info = request.query_params.get('extra_info')

        if case == 'success':
            return self.success(extra_info=extra_info)
        elif case == 'bad_request':
            return self.bad_request(extra_info=extra_info)
        elif case == 'forbidden':
            return self.forbidden(extra_info=extra_info)
        elif case == 'internal_server_error':
            return self.internal_server_error(extra_info=extra_info)

    def post(self, request):
        append_dict = request.data.dict()

        extra_kwargs = {**test_extra_kwargs, **append_dict}
        lookup_map = {**test_lookup_map, **append_dict}
        filter_map = {**test_filter_map, **append_dict}
        inspect_map = {**test_inspect_map}

        assert self.get_extra_kwargs(**append_dict) == extra_kwargs
        assert self.get_lookup_map(**append_dict) == lookup_map
        assert self.get_filter_map(**append_dict) == filter_map
        assert self.get_cur_inspect_map() == inspect_map

        handler = self.get_jackal_exception_handler()
        assert handler is jackal_exception_handler

        inspector = self.get_inspector(request)

        assert isinstance(inspector, self.inspector_class)

        return self.success()


class APIViewExtraTest(JackalAPITestCase):
    def test_getter(self):
        append_dict = {'g': 'h'}
        response = self.client.post('/extra', append_dict)
        self.assertSuccess(response)

    def test_response(self):
        case = 'success'
        response = self.client.get('/extra', {'case': case, 'extra_info': 'extra_info'})
        self.assertSuccess(response)
        self.assertIn('extra_info', response.json())
        self.assertEqual('extra_info', response.json()['extra_info'])

        case = 'bad_request'
        response = self.client.get('/extra', {'case': case, 'extra_info': 'extra_info'})
        self.assertStatusCode(400, response)
        self.assertIn('extra_info', response.json())
        self.assertEqual('extra_info', response.json()['extra_info'])

        case = 'forbidden'
        response = self.client.get('/extra', {'case': case, 'extra_info': 'extra_info'})
        self.assertStatusCode(403, response)
        self.assertIn('extra_info', response.json())
        self.assertEqual('extra_info', response.json()['extra_info'])

        case = 'internal_server_error'
        response = self.client.get('/extra', {'case': case, 'extra_info': 'extra_info'})
        self.assertStatusCode(500, response)
        self.assertIn('extra_info', response.json())
        self.assertEqual('extra_info', response.json()['extra_info'])
