from rest_framework import serializers

from jackal.paginators import JackalPaginator
from jackal.settings import jackal_settings
from jackal.shortcuts import model_update
from jackal.views.base import JackalAPIView

__all__ = [
    'BaseListCreateGeneric',
    'BaseDetailUpdateDestroyGeneric',
    'PaginateListGeneric',
    'SimpleGeneric',
]


class BaseListCreateGeneric(JackalAPIView):
    serializer_class = None
    list_mixin = None
    create_mixin = None

    def list(self, request, **kwargs):
        if self.list_mixin is None:
            serializer_class = self.get_serializer_class()
            filtered_queryset = self.get_filtered_queryset(request, **kwargs)
            ser = serializer_class(instance=filtered_queryset, many=True)
            return self.simple_response(ser.data)
        else:
            return self.simple_response(self.list_mixin(request, **kwargs))

    def create(self, request, **kwargs):
        if self.create_mixin is None:
            data = self.get_valid_data(request)
            obj = self.get_model().objects.create(**data)
            return self.success(id=obj.id)
        else:
            result = self.create_mixin(request, **kwargs)
            if result is True or result is None:
                return self.success()
            else:
                return self.simple_response(result)


class BaseDetailUpdateDestroyGeneric(JackalAPIView):
    update_mixin = None
    detail_mixin = None
    destroy_mixin = None

    def detail(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if self.detail_mixin is None:
            ser = self.serializer_class(obj)
            return self.simple_response(ser.data)
        else:
            data = self.detail_mixin(obj)
            return self.simple_response(data)

    def update(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if self.update_mixin is None:
            data = self.get_valid_data(request)
            model_update(obj, **data)
            return self.success(id=obj.id)

        else:
            result = self.update_mixin(request, obj)
            return self.simple_response(result)

    def destroy(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if self.destroy_mixin is None:
            obj.delete()
            return self.success()
        else:
            result = self.destroy_mixin(request, obj)
            return self.simple_response(result)


class PaginateListGeneric(JackalAPIView):
    default_page = 1
    default_limit = None

    def paginated_list(self, request, **kwargs):
        queryset = self.get_filtered_queryset(request, **kwargs)
        return self.paginated_data(request, queryset)

    def paginated_data(self, request, queryset):
        if self.default_limit is None:
            self.default_limit = jackal_settings.PAGE_LENGTH

        paginator = JackalPaginator(queryset, request, self.default_page, self.default_limit)
        response_data = paginator.serialized_data(self.get_serializer_class(), self.get_serializer_context())
        return self.simple_response(response_data)


class SimpleGeneric(JackalAPIView):
    def wrapper(self, request, method='get', **kwargs):
        return getattr(self, '{}_func'.format(method))(request, **kwargs)

    def get_func(self, request, **kwargs):
        pass

    def post_func(self, request, **kwargs):
        pass

    def patch_func(self, request, **kwargs):
        pass

    def delete_func(self, request, **kwargs):
        pass


class LabelValueListGeneric(JackalAPIView):
    label_field = 'name'
    value_field = 'id'

    def get_serializer_class(self):
        class LabelValueSerializer(serializers.ModelSerializer):
            label = serializers.CharField(source=self.label_field)
            value = serializers.CharField(source=self.value_field)

            class Meta:
                model = self.model
                fields = ('label', 'value')

        return LabelValueSerializer

    def get(self, request, **kwargs):
        queryset = self.get_filtered_queryset(request, **kwargs)
        ser_class = self.get_serializer_class()
        return self.simple_response(ser_class(queryset, many=True))


class DetailMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)


class DestroyMixin(BaseDetailUpdateDestroyGeneric):
    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class UpdateMixin(BaseDetailUpdateDestroyGeneric):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DetailUpdateMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DetailUpdateDestroyMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class DetailDestroyMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class UpdateDestroyMixin(BaseDetailUpdateDestroyGeneric):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class ListMixin(BaseListCreateGeneric):
    def get(self, request, **kwargs):
        return self.list(request, **kwargs)


class CreateMixin(BaseListCreateGeneric):
    def post(self, request, **kwargs):
        return self.create(request, **kwargs)


class ListCreateMixin(BaseListCreateGeneric):
    def get(self, request, **kwargs):
        return self.list(request, **kwargs)

    def post(self, request, **kwargs):
        return self.create(request, **kwargs)


class PaginateListMixin(PaginateListGeneric):
    def get(self, request, **kwargs):
        return self.paginated_list(request, **kwargs)


class PostMixin(SimpleGeneric):
    def post(self, request, **kwargs):
        return self.wrapper(request, method='post', **kwargs)


class GetMixin(SimpleGeneric):
    def get(self, request, **kwargs):
        return self.wrapper(request, method='get', **kwargs)


class PutMixin(SimpleGeneric):
    def put(self, request, **kwargs):
        return self.wrapper(request, method='put', **kwargs)


class PatchMixin(SimpleGeneric):
    def patch(self, request, **kwargs):
        return self.wrapper(request, method='patch', **kwargs)


class DeleteMixin(SimpleGeneric):
    def delete(self, request, **kwargs):
        return self.wrapper(request, method='delete', **kwargs)


class LabelValueListMixin(LabelValueListGeneric):
    pass
