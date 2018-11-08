from rest_framework.views import APIView

from jackal.filters import JackalQueryFilter
from jackal.helpers.dict_helper import JackalDictMapper
from jackal.inspectors import BaseInspector
from jackal.settings import jackal_settings
from jackal.views.simplizer import ResponseSimplizer


class _Getter:
    model = None
    queryset = None
    serializer_class = None
    inspect_map = None
    inspector_class = BaseInspector

    def get_queryset(self):
        return self.queryset

    def get_model(self):
        return self.model

    def get_lookup_map(self, **additional):
        d = self.lookup_map
        d.update(additional)
        return d

    def get_filter_map(self, **additional):
        d = self.filter_map
        d.update(additional)
        return d

    def get_extra_kwargs(self, **additional):
        d = self.extra_kwargs
        d.update(additional)
        return d

    def get_query_filter_class(self):
        if self.query_filter is None:
            return JackalQueryFilter
        return self.query_filter

    def get_serializer_class(self, request):
        return self.serializer_class

    def get_serializer_context(self):
        return {}

    def get_jackal_exception_handler(self):
        return jackal_settings.EXCEPTION_HANDLER

    def get_inspector(self, request):
        inspect_map = self.get_inspect_map(request.method)
        if not inspect_map:
            return dict()
        ins_class = self.inspector_class
        return ins_class(request.data, inspect_map)

    def get_inspect_map(self, method=''):
        if not method:
            return self.inspect_map

        inspect_map = getattr(self, '{}_inspect_map'.format(method), self.inspect_map)
        return inspect_map

    def get_inspect_data(self, request):
        inspector = self.get_inspector(request)
        return inspector.inspected_data


class _Override:
    def dispatch(self, request, *args, **kwargs):
        self.pre_dispatch(request, *args, **kwargs)
        response = super().dispatch(request, *args, **kwargs)
        self.post_dispatch(request, response, *args, **kwargs)
        return response

    def pre_dispatch(self, request, *args, **kwargs):
        """
        This will call before dispatch. before permission check, before authenticate, before initial request...
        """
        pass

    def post_dispatch(self, request, response, *args, **kwargs):
        """
        This will call after dispatch. after all api view logic. So it receive response to argument.
        """
        pass

    def handle_exception(self, exc):
        """
        high jacking exception and handle with jackal_exception_handler
        """
        jackal_handler = self.get_jackal_exception_handler()
        context = self.get_exception_handler_context()
        response = jackal_handler(exc, context)
        if response is not None:
            response.exception = True
            return response
        else:
            return super().handle_exception(exc)

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        request.inspect_data = self.get_inspect_data(request)
        return request


class JackalBaseAPIView(APIView, _Getter, _Override):
    default_permission_classes = ()
    default_authentication_classes = ()

    permission_classes = ()
    authentication_classes = ()

    lookup_map = {}
    filter_map = {}

    search_dict = {}
    extra_kwargs = {}

    user_field = ''

    query_filter = JackalQueryFilter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_classes += self.default_permission_classes
        self.authentication_classes += self.default_authentication_classes

    def get_object(self, request, **kwargs):
        f_class = self.get_query_filter_class()
        f = f_class(queryset=self.get_model().objects.all(), params=request.query_params)

        lookup_map = self.get_lookup_map()
        extra_kwargs = self.get_extra_kwargs(**JackalDictMapper.av2bv(lookup_map, kwargs))

        obj = f.extra(**extra_kwargs).get(raise_404=True)
        self.check_object_permissions(request=request, obj=obj)
        return obj

    def get_filtered_queryset(self, request, **kwargs):
        f_class = self.get_query_filter_class()
        f = f_class(queryset=self.get_queryset(), params=request.query_params)

        lookup_map = self.get_lookup_map()
        filter_map = self.get_filter_map()

        if self.user_field:
            extra_kwargs = self.get_extra_kwargs(**{self.user_field: request.user})
        else:
            extra_kwargs = self.get_extra_kwargs()

        extra_kwargs.update(JackalDictMapper.av2bv(lookup_map, kwargs))
        f = f.filter_map(filter_map).extra(**extra_kwargs)
        return f.queryset


class JackalAPIView(JackalBaseAPIView, ResponseSimplizer):
    pass
