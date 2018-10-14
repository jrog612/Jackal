from django.db import transaction

from jackal.base import JackalAPIView
from jackal.paginator import SerializerPaginator
from jackal.shortcuts import model_update, status_setter

__all__ = [
    'BaseListCreateGeneric',
    'BaseDetailUpdateDestroyGeneric',
    'PaginateListGeneric',
    'SimpleGeneric',
    # 'StatusChangeGeneric',
]


class BaseListCreateGeneric(JackalAPIView):
    queryset = None
    serializer_class = None
    lookup_map = {}
    filter_map = {}
    list_mixin = None
    create_mixin = None

    def list(self, request, **kwargs):
        if self.list_mixin is None:
            ser = self.serializer_class(instance=self.get_queryset(request, **kwargs), many=True)
            return self.response(ser.data)
        else:
            return self.response(self.list_mixin(request, **kwargs))

    def create(self, request, **kwargs):
        if self.create_mixin is None:
            data = self.get_valid_data(request)
            obj = self.model.objects.create(**data)
            return self.success(id=obj.id)

        else:
            result = self.create_mixin(request, **kwargs)

            if result is True or not result:
                return self.success()
            else:
                return self.response(result)


class BaseDetailUpdateDestroyGeneric(JackalAPIView):
    update_mixin = None
    detail_mixin = None
    destroy_mixin = None

    def detail(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if self.detail_mixin is None:
            ser = self.serializer_class(obj)
            return self.response(ser.data)
        else:
            data = self.detail_mixin(obj)
            return self.response(data)

    def update(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if self.update_mixin is None:
            data = self.get_valid_data(request)
            model_update(obj, **data)
            return self.success(id=obj.id)

        else:
            result = self.update_mixin(request, obj)
            return self.response(result)

    def destroy(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if self.destroy_mixin is None:
            obj.delete()
            return self.success()
        else:
            result = self.destroy_mixin(request, obj)
            return self.response(result)


class PaginateListGeneric(JackalAPIView):
    default_page = 1
    default_limit = 10

    def paginated_list(self, request, **kwargs):
        queryset = self.get_queryset(request, **kwargs)
        return self.paginated_data(request, queryset)

    def paginated_data(self, request, queryset):
        page = request.query_params.get('page_number', self.default_page)
        if int(page) <= 0:
            page = 1
        limit = request.query_params.get('page_length', self.default_limit)
        paginator = SerializerPaginator(queryset, self.serializer_class, page, limit)
        return self.response(paginator.response_data)


class SimpleGeneric(JackalAPIView):
    def wrapper(self, request, method='get', **kwargs):
        return getattr(self, f'{method}_func')(request, **kwargs)

    def get_func(self, request, **kwargs):
        pass

    def post_func(self, request, **kwargs):
        pass

    def patch_func(self, request, **kwargs):
        pass

    def delete_func(self, request, **kwargs):
        pass
