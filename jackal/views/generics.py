from django.db import transaction

from jackal.base import JackalAPIView
from jackal.paginator import SerializerPaginator
from jackal.shortcuts import model_update

__all__ = [
    'BaseListCreateGeneric',
    'BaseDetailUpdateDestroyGeneric',
    'PaginateListGeneric',
    'SimpleGeneric',
    'StatusChangeGeneric',
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


# class StatusChangeGeneric(JackalAPIView):
#     """
#     상태값 변경에 있어 자동으로 유효성 검사 및 변경을 진행해주는 제네릭입니다.
#     status_setter 를 이용하여 상태를 변경하며, 구조체 STATUS_CONDITION 에 정의된 조건에 따라 검사를 진행합니다.
#     검사 중 실패할 경우 403 에러와 함께 사용자에게 바로 보여줘도 되는 메세지를 제공합니다.
#
#     요청은 POST 를 이용합니다.
#
#     사용법:
#         * model (필수)
#         * lookup_map (필수)
#         * status (필수) : 변경할 상태값
#         * key (필수) : STATUS_CONDITION 구조체 및 STATUS_MAPPER 구조체 등에서 공통적으로 사용하는 key 입니다. {모델 소문자_필드명 소문자} 형태로 지정하면 됩니다.
#         * status_field : 변경할 상태필드 명입니다. 기본 값은 `status` 입니다.
#         * status_setter : 직접 지정할 상태 변경자. 없다면 기본 `status_setter`를 이용함.
#
#     """
#
#     status = None
#     key = None
#     status_field = 'status'
#     status_setter = None
#
#     def change(self, request, **kwargs):
#         obj = self.get_object(request, **kwargs)
#         # 현재 상태 값을 가져온다.
#         current_status = getattr(obj, self.status_field)
#         with transaction.atomic():
#             # 지정된 스테이터스 세터가 있다면, 그 status_setter 를 이용해 상태를 설정한다.
#             if self.status_setter is not None:
#                 result = self.status_setter(obj, self.status)
#             else:
#                 # 그게 아니라면, 기본 status_setter 를 이용한다.
#                 result = status_setter(obj, self.status, self.key, status_field=self.status_field)
#             # 결과 값이 False, None 등이라면 아래의 예외를 raise
#             if not result:
#                 raise StatusChangeException(self.key, current_status, self.status)
#         return self.success()
