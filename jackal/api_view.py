from rest_framework.response import Response
from rest_framework.views import APIView

from jackal.filter import JackalQueryFilter
from jackal.helpers.dict_helper import JackalDictMapper
from jackal.settings import jackal_settings
from jackal.shortcuts import valid_data


class _GetterMixin:
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

    def get_request_filter_class(self):
        if self.request_filter is None:
            return JackalQueryFilter
        return self.request_filter

    def get_valid_data(self, request):
        return valid_data(request.data, self.valid_key)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {}

    def get_jackal_exception_handler(self):
        return jackal_settings.EXCEPTION_HANDLER


class _ResponseMixin:
    @staticmethod
    def success(detail='success', **kwargs):
        return Response({'detail': detail, **kwargs})

    @staticmethod
    def simple_response(result=None, status=200, headers=None, **kwargs):
        return Response(result, status=status, headers=headers, **kwargs)

    @staticmethod
    def bad_request(data):
        return Response(data, status=400)

    @staticmethod
    def forbidden(data):
        return Response(data, status=403)

    @staticmethod
    def internal_server_error(data):
        return Response(data, status=500)


class JackalAPIView(APIView, _ResponseMixin, _GetterMixin):
    default_permission_classes = ()
    default_authentication_classes = ()

    permission_classes = ()
    authentication_classes = ()

    model = None
    queryset = None
    serializer_class = None
    lookup_map = {}
    extra_kwargs = {}
    filter_map = {}
    search_dict = {}

    user_field = ''
    valid_key = ''

    query_filter = JackalQueryFilter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_classes += self.default_permission_classes
        self.authentication_classes += self.default_authentication_classes

    def pre_dispatch(self, request, *args, **kwargs):
        """
        This will call before dispatch. before permission check, before authenticate, before initial request...
        """
        pass

    def dispatch(self, request, *args, **kwargs):
        self.pre_dispatch(request, *args, **kwargs)
        response = super().dispatch(request, *args, **kwargs)
        self.post_dispatch(request, response, *args, **kwargs)
        return response

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

    def get_object(self, request, **kwargs):
        f_class = self.get_request_filter_class()
        f = f_class(queryset=self.get_model().objects.all(), params=request.query_params)

        lookup_map = self.get_lookup_map()
        extra_kwargs = self.get_extra_kwargs(**JackalDictMapper.av2bv(lookup_map, kwargs))

        obj = f.extra(**extra_kwargs).get_obj(raise_404=True)
        self.check_object_permissions(request=request, obj=obj)
        return obj

    def get_filtered_queryset(self, request, **kwargs):
        f_class = self.get_request_filter_class()
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
