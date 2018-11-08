from rest_framework.views import APIView

from jackal.filters import JackalQueryFilter
from jackal.helpers.dict_helper import JackalDictMapper
from jackal.inspectors import BaseInspector
from jackal.settings import jackal_settings
from jackal.views.simplizer import ResponseSimplizer


class _Getter:
    def get_queryset(self, request):
        return self.queryset

    def get_model(self, request):
        return self.model

    def get_lookup_map(self, request, **additional):
        d = self.lookup_map
        d.update(additional)
        return d

    def get_filter_map(self, request, **additional):
        d = self.filter_map
        d.update(additional)
        return d

    def get_extra_kwargs(self, request, **additional):
        d = self.extra_kwargs
        d.update(additional)
        return d

    def get_query_filter_class(self, request):
        if self.query_filter is None:
            return JackalQueryFilter
        return self.query_filter

    def get_serializer_class(self, request):
        return self.serializer_class

    def get_serializer_context(self, request):
        return {}

    def get_jackal_exception_handler(self, request):
        return jackal_settings.EXCEPTION_HANDLER

    def get_inspector(self, request):
        inspect_map = self.get_inspect_map(request)
        if not inspect_map:
            return dict()
        ins_class = self.inspector_class
        return ins_class(request.data, inspect_map)

    def get_inspect_map(self, request):
        if not request:
            return self.inspect_map

        inspect_map = getattr(self, '{}_inspect_map'.format(request), self.inspect_map)
        return inspect_map

    def get_inspect_data(self, request):
        inspector = self.get_inspector(request)
        return inspector.inspected_data

    def get_user_field(self, request):
        return self.user_field


class _Override:
    """
    Override class contains overriding methods in APIView of rest framework
    """

    def dispatch(self, request, *args, **kwargs):
        self.pre_dispatch(request, *args, **kwargs)
        response = super().dispatch(request, *args, **kwargs)
        self.post_dispatch(request, response, *args, **kwargs)
        return response

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

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.pre_method_call(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        super().post_method_call(request, response, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)

    def check_permissions(self, request):
        self.pre_check_permissions(request)
        super().check_permissions(request)
        self.post_check_permissions(request)

    def check_object_permissions(self, request, obj):
        self.pre_check_object_permissions(request, obj)
        super().check_object_permissions(request, obj)
        self.post_check_object_permissions(request, obj)


class _PrePost:
    def pre_method_call(self, request, *args, **kwargs):
        """
        This will call before method run. Likes get, post, patch...
        """
        pass

    def post_method_call(self, request, response, *args, **kwargs):
        """
        This will call after method run. Likes get, post, patch...
        """
        pass

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

    def pre_check_permissions(self, request):
        pass

    def post_check_permissions(self, request):
        pass

    def pre_check_object_permissions(self, request, obj):
        pass

    def post_check_object_permissions(self, request, obj):
        pass


class JackalBaseAPIView(APIView, _Getter, _Override, _PrePost):
    default_permission_classes = ()
    default_authentication_classes = ()
    permission_classes = ()
    authentication_classes = ()

    model = None
    queryset = None

    lookup_map = {}
    filter_map = {}
    search_dict = {}
    extra_kwargs = {}
    inspect_map = None
    user_field = ''

    serializer_class = None
    query_filter = JackalQueryFilter
    inspector_class = BaseInspector

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_classes += self.default_permission_classes
        self.authentication_classes += self.default_authentication_classes

    def get_object(self, request, **kwargs):
        queryset = self.get_user_queryset(self.get_model(request).objects.all(), request)

        f_class = self.get_query_filter_class(request)
        f = f_class(queryset=queryset, params=request.query_params)

        lookup_map = self.get_lookup_map(request)
        extra_kwargs = self.get_extra_kwargs(**JackalDictMapper.av2bv(lookup_map, kwargs))

        obj = f.extra(**extra_kwargs).get(raise_404=True)
        self.check_object_permissions(request=request, obj=obj)
        return obj

    def get_filtered_queryset(self, request, **kwargs):
        queryset = self.get_user_queryset(self.get_queryset(request), request)

        f_class = self.get_query_filter_class(request)
        f = f_class(queryset=queryset, params=request.query_params)

        lookup_map = self.get_lookup_map(request)
        filter_map = self.get_filter_map(request)
        extra_kwargs = self.get_extra_kwargs(request)
        extra_kwargs.update(JackalDictMapper.av2bv(lookup_map, kwargs))

        queryset = f.filter_map(filter_map).extra(**extra_kwargs).queryset
        return queryset

    def get_user_queryset(self, queryset, request):
        user_field = self.get_user_field(request)
        if user_field is not None:
            queryset = queryset.filter(**{user_field: request.user})

        return queryset


class JackalAPIView(JackalBaseAPIView, ResponseSimplizer):
    pass
