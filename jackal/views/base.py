from rest_framework.response import Response
from rest_framework.views import APIView

from jackal.filters import JackalQueryFilter
from jackal.helpers.data_helper import JackalDictMapper
from jackal.inspectors import Inspector
from jackal.paginators import JackalPaginator
from jackal.settings import jackal_settings


class _Getter:
    def get_queryset(self):
        return self.queryset

    def get_model(self):
        if self.model is not None:
            return self.model
        else:
            return self.get_queryset().model

    def get_lookup_map(self, **additional):
        d = self.lookup_map or dict()
        return {**d, **additional}

    def get_filter_map(self, **additional):
        d = self.filter_map or dict()
        return {**d, **additional}

    def get_search_dict(self, **additional):
        d = self.search_dict or dict()
        return {**d, **additional}

    def get_extra_kwargs(self, **additional):
        d = self.extra_kwargs or dict()
        return {**d, **additional}

    def get_query_filter_class(self):
        if self.query_filter is None:
            return JackalQueryFilter
        return self.query_filter

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self, **kwargs):
        return kwargs

    def get_serializer_data(self, instance, context=None, many=False, klass=None):
        if klass is None:
            klass = self.get_serializer_class()
        context = self.get_serializer_context(**(context or dict()))
        ser = klass(instance, many=many, context=context)
        return ser.data

    def get_jackal_exception_handler(self):
        return jackal_settings.EXCEPTION_HANDLER

    def get_inspector(self, request):
        inspect_map = self.get_cur_inspect_map()
        if not inspect_map:
            return None
        ins_class = self.inspector_class
        return ins_class(request.data, inspect_map)

    def get_cur_inspect_map(self):
        return getattr(self, '{}_inspect_map'.format(self.request.method), self.inspect_map)

    def get_user_field(self):
        return self.user_field

    def get_permission_classes(self):
        return self.default_permission_classes + self.permission_classes

    def get_authentication_classes(self):
        return self.default_authentication_classes + self.authentication_classes

    def get_authenticators(self):
        return [auth() for auth in self.get_authentication_classes()]

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


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

    def pre_check_permissions(self, request):
        pass

    def post_check_permissions(self, request):
        pass

    def pre_check_object_permissions(self, request, obj):
        pass

    def post_check_object_permissions(self, request, obj):
        pass

    def pre_handle_exception(self, exc):
        pass


class JackalBaseAPIView(_Getter, _PrePost, APIView):
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
    inspect_map = {}

    user_field = ''
    bind_user_field = None

    result_root = None
    result_meta = 'meta'

    default_page_number = 1
    default_page_length = None

    search_keyword_key = 'search_keyword'
    search_type_key = 'search_type'
    page_number_key = 'page_number'
    page_length_key = 'page_length'
    ordering_key = 'ordering'

    serializer_class = None
    query_filter = JackalQueryFilter
    inspector_class = Inspector
    paginator_class = JackalPaginator

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            self.initial(request, *args, **kwargs)
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            self.pre_method_call(request, *args, **kwargs)
            response = handler(request, *args, **kwargs)
            self.post_method_call(request, response, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        return self.response

    def handle_exception(self, exc):
        """
        high jacking exception and handle with jackal_exception_handler
        """
        self.pre_handle_exception(exc)
        jackal_handler = self.get_jackal_exception_handler()
        context = self.get_exception_handler_context()
        response = jackal_handler(exc, context)
        if response is not None:
            response.exception = True
            return response
        else:
            return super().handle_exception(exc)

    def check_permissions(self, request):
        self.pre_check_permissions(request)
        super().check_permissions(request)
        self.post_check_permissions(request)

    def check_object_permissions(self, request, obj):
        self.pre_check_object_permissions(request, obj)
        super().check_object_permissions(request, obj)
        self.post_check_object_permissions(request, obj)

    def get_object(self, request, **kwargs):
        queryset = self.get_user_queryset(queryset=self.get_model().objects.all(), request=request)

        f_class = self.get_query_filter_class()
        f = f_class(queryset=queryset, params=request.query_params)

        lookup_map = self.get_lookup_map()
        extra_kwargs = self.get_extra_kwargs(**JackalDictMapper.av2bv(lookup_map, kwargs))

        obj = f.extra(**extra_kwargs).get(raise_404=True)
        self.check_object_permissions(request=request, obj=obj)
        return obj

    def get_filtered_queryset(self, request, **kwargs):
        queryset = self.get_user_queryset(queryset=self.get_queryset(), request=request)

        f_class = self.get_query_filter_class()
        f = f_class(queryset=queryset, params=request.query_params)

        lookup_map = self.get_lookup_map()
        filter_map = self.get_filter_map()
        search_dict = self.get_search_dict()
        extra_kwargs = self.get_extra_kwargs()
        extra_kwargs.update(JackalDictMapper.av2bv(lookup_map, kwargs))

        queryset = f.search(
            search_dict,
            search_keyword_key=self.search_keyword_key,
            search_type_key=self.search_type_key
        ).filter_map(filter_map).extra(
            **extra_kwargs
        ).ordering(
            self.ordering_key
        ).queryset.distinct()
        return queryset

    def get_user_queryset(self, request, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        user_field = self.get_user_field()
        if user_field:
            queryset = queryset.filter(**{user_field: request.user})

        return queryset

    def get_inspected_data(self, request):
        inspector = self.get_inspector(request)
        if inspector is not None:
            return inspector.inspected_data
        return dict()

    def get_paginator_class(self):
        return self.paginator_class

    def get_response_data(self, request, **kwargs):
        pass

    def has_auth(self):
        return self.request.user is not None and self.request.user.is_authenticated

    def _response(self, result=None, status=200, meta=None, headers=None, **kwargs):
        response_data = {}

        if self.result_root:
            response_data[self.result_root] = result
        else:
            response_data = result

        if self.result_meta:
            response_data[self.result_meta] = meta or dict()

        return Response(response_data, status=status, headers=headers, **kwargs)

    def simple_response(self, result=None, status=200, meta=None, headers=None, **kwargs):
        return self._response(result, status=status, meta=meta, headers=headers, **kwargs)

    def binding_user(self):
        return self.request.user


class JackalAPIView(JackalBaseAPIView):
    pass
