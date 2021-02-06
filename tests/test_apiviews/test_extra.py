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

        inspector = self.get_inspector()

        assert isinstance(inspector, self.inspector_class)

        return self.simple_response()


class APIViewExtraTest(JackalAPITestCase):
    def test_getter(self):
        append_dict = {'g': 'h'}
        response = self.client.post('/extra', append_dict)
        self.assertSuccess(response)
