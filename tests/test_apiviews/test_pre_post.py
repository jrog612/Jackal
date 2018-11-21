from jackal.tests import JackalAPITestCase
from jackal.views.base import JackalAPIView
from tests.models import TestModel


class PrePostRaise(BaseException):
    def __init__(self, kind):
        self.kind = kind


class PrePostTestAPI(JackalAPIView):
    model = TestModel
    extra_kwargs = {'field_int': 1}

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PrePostRaise as e:
            assert e.kind == kwargs['kind']
            self.response = super().finalize_response(
                request, self.simple_response({'kind': kwargs['kind']}, status=400), skip=True, *args, **kwargs
            )
            return self.response

    def post(self, request, **kwargs):
        self.get_object(request, **kwargs)
        return self.success()

    def pre_check_object_permissions(self, request, obj):
        if self.kwargs['kind'] == 'pre_check_object_permissions':
            raise PrePostRaise('pre_check_object_permissions')

    def post_check_object_permissions(self, request, obj):
        if self.kwargs['kind'] == 'post_check_object_permissions':
            raise PrePostRaise('post_check_object_permissions')

    def pre_check_permissions(self, request):
        if self.kwargs['kind'] == 'pre_check_permissions':
            raise PrePostRaise('pre_check_permissions')

    def post_check_permissions(self, request):
        if self.kwargs['kind'] == 'post_check_permissions':
            raise PrePostRaise('post_check_permissions')

    def pre_method_call(self, request, *args, **kwargs):
        if kwargs['kind'] == 'pre_method_call':
            raise PrePostRaise('pre_method_call')

    def post_method_call(self, request, response, *args, **kwargs):
        if kwargs['kind'] == 'post_method_call':
            raise PrePostRaise('post_method_call')


class PrePostTest(JackalAPITestCase):
    pre_check_list = [
        'pre_check_object_permissions',
        'pre_check_permissions',
        'pre_method_call',
    ]

    post_check_list = [
        'post_check_object_permissions',
        'post_check_permissions',
        'post_method_call',
    ]

    def setUp(self):
        TestModel.objects.create(field_int=1)

    def test_pre(self):
        for i in self.pre_check_list:
            response = self.client.post('/pre-post/{}'.format(i))
            result = response.json()
            self.assertStatusCode(400, response)
            self.assertEqual(result['kind'], i)

    def test_post(self):
        for i in self.post_check_list:
            response = self.client.post('/pre-post/{}'.format(i))
            result = response.json()
            self.assertStatusCode(400, response)
            self.assertEqual(result['kind'], i)
