from rest_framework import serializers

from jackal.shortcuts import model_update
from jackal.views.base import JackalAPIView


class ListCreateGeneric(JackalAPIView):
    def get_response_data(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        filtered_queryset = self.get_filtered_queryset(request, **kwargs)
        ser = serializer_class(instance=filtered_queryset, many=True, context=self.get_serializer_context())
        return ser.data

    def list(self, request, **kwargs):
        response_data = self.get_response_data(request, **kwargs)
        return self.simple_response(response_data)

    def create(self, request, **kwargs):
        model = self.get_model()
        obj = model(**self.get_inspected_data(request))
        if self.bind_user_field:
            setattr(obj, self.bind_user_field, self.binding_user())
        obj.save()
        return self.simple_response({'id': obj.id})


class DetailUpdateDestroyGeneric(JackalAPIView):
    def get_response_data(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        ser = self.serializer_class(obj, context=self.get_serializer_context())
        return ser.data

    def detail(self, request, **kwargs):
        response_data = self.get_response_data(request, **kwargs)
        return self.simple_response(response_data)

    def update(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        model_update(obj, **self.get_inspected_data(request))
        return self.simple_response({'id': obj.id})

    def destroy(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        obj.delete()
        return self.simple_response()


class PaginateListGeneric(JackalAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paginator = None

    def get_paginator(self, request, queryset):
        page_num = request.query_params.get(self.page_number_key, self.default_page_number)
        page_length = request.query_params.get(self.page_length_key, self.default_page_length)

        paginator_class = self.get_paginator_class()
        return paginator_class(queryset, page_num, page_length)

    def get_response_data(self, request, **kwargs):
        queryset = self.get_filtered_queryset(request, **kwargs)
        self.paginator = self.get_paginator(request, queryset)
        paginated_data = self.paginator.serialized_data(
            serializer_class=self.get_serializer_class(),
            context=self.get_serializer_context()
        )
        return paginated_data

    def paginated_list(self, request, **kwargs):
        result = self.get_response_data(request, **kwargs)
        meta_data = self.paginator.meta_data()
        return self.simple_response(result, meta=meta_data)


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
        serialized_data = ser_class(queryset, many=True)
        return self.simple_response(serialized_data.data)


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
