from rest_framework import serializers

from jackal.paginators import JackalPaginator
from jackal.shortcuts import model_update
from jackal.views.base import JackalAPIView


class ListCreateGeneric(JackalAPIView):
    def list(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        filtered_queryset = self.get_filtered_queryset(request, **kwargs)
        ser = serializer_class(instance=filtered_queryset, many=True, context=self.get_serializer_context())
        return self.simple_response(ser.data)

    def create(self, request, **kwargs):
        model = self.get_model()
        obj = model.objects.create(**request.inspected_data)
        return self.success(id=obj.id)


class DetailUpdateDestroyGeneric(JackalAPIView):
    def detail(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        ser = self.serializer_class(obj, context=self.get_serializer_context())
        return self.simple_response(ser.data)

    def update(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        model_update(obj, **request.inspected_data)
        return self.success(id=obj.id)

    def destroy(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        obj.delete()
        return self.success()


class PaginateListGeneric(JackalAPIView):
    default_page_number = 1
    default_page_length = None
    page_number_key = 'page_number'
    page_length_key = 'page_length'

    def paginated_list(self, request, **kwargs):
        queryset = self.get_filtered_queryset(request, **kwargs)
        return self.paginated_data(request, queryset)

    def paginated_data(self, request, queryset):
        page_num = request.query_params.get(self.page_number_key, self.default_page_number)
        page_length = request.query_params.get(self.page_length_key, self.default_page_length)
        paginator = JackalPaginator(queryset, page_num, page_length)
        response_data = paginator.serialized_data(
            self.get_serializer_class(), self.get_serializer_context()
        )
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
                model = self.get_model()
                fields = ('label', 'value')

        return LabelValueSerializer

    def label_value_list(self, request, **kwargs):
        queryset = self.get_filtered_queryset(request, **kwargs)
        ser_class = self.get_serializer_class()
        return self.simple_response(ser_class(queryset, many=True))


class DetailMixin(DetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)


class DestroyMixin(DetailUpdateDestroyGeneric):
    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class UpdateMixin(DetailUpdateDestroyGeneric):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DetailUpdateMixin(DetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DetailUpdateDestroyMixin(DetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class DetailDestroyMixin(DetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class UpdateDestroyMixin(DetailUpdateDestroyGeneric):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class ListMixin(ListCreateGeneric):
    def get(self, request, **kwargs):
        return self.list(request, **kwargs)


class CreateMixin(ListCreateGeneric):
    def post(self, request, **kwargs):
        return self.create(request, **kwargs)


class ListCreateMixin(ListCreateGeneric):
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
    def get(self, request, **kwargs):
        return self.label_value_list(request, **kwargs)
