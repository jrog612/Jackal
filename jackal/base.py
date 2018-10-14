from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from jackal.exceptions import jackal_exception_handler
from jackal.filter import JackalRequestFilter
from jackal.shortcuts import valid_data


class JackalAPIView(APIView):
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
    user_field = ''
    valid_key = ''
    search_type = ''
    request_filter = JackalRequestFilter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_classes += self.default_permission_classes
        self.authentication_classes += self.default_authentication_classes

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
        high jacking exception
        """
        response = jackal_exception_handler(exc)
        if response is not None:
            response.exception = True
            return response
        else:
            return super().handle_exception(exc)

    def get_request_filter_class(self):
        return self.request_filter

    def make_lookup_map_filterable(self, kwargs):
        return {map_value: kwargs.get(map_key) for map_key, map_value in self.lookup_map.items()}

    def get_object(self, request, **kwargs):
        query_dict = self.make_lookup_map_filterable(kwargs)
        query_dict.update(self.extra_kwargs)

        obj = get_object_or_404(
            self.model,
            **query_dict
        )
        self.check_object_permissions(request=request, obj=obj)
        return obj

    def get_queryset(self, request, **kwargs):
        queryset = self.queryset

        query_dict = self.make_lookup_map_filterable(kwargs)

        if self.user_field:
            query_dict[self.user_field] = request.user

        # 1차 lookup_map 필터링
        queryset = queryset.filter(**query_dict)

        # 2차 filter_map 필터링
        request_filter_class = self.get_request_filter_class()
        queryset = request_filter_class(queryset, request.query_params, self.filter_map).data

        self.queryset = queryset
        return queryset

    def get_valid_data(self, request):
        return valid_data(request.data, self.valid_key)

    @staticmethod
    def success(detail='success', **kwargs):
        return Response({'detail': detail, **kwargs})

    @staticmethod
    def response(result=None, status=200, headers=None, **kwargs):
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


class JackalAPIException(APIException):
    default_message = ''
    status_code = ''

    def __str__(self):
        return self.__class__.__name__

    def response_data(self):
        return {}


class MessageException(JackalAPIException):
    default_message = ''

    def __init__(self, message=None, extra_data=None, **kwargs):
        if message is None:
            self.message = self.default_message
        else:
            self.message = message
        self.extra_data = extra_data
        self.kwargs = kwargs

    def response_data(self):
        return {'message': self.message, **self.kwargs}
