from django.core.paginator import EmptyPage, Paginator

from jackal.settings import jackal_settings


class JackalPaginator:
    def __init__(self, queryset, request, page_number, page_length):
        if page_length is None:
            page_length = jackal_settings.PAGE_LENGTH if jackal_settings.PAGE_LENGTH else 10

        self.paginator = Paginator(queryset, page_length)
        self.page_number = int(page_number)
        self.page_length = int(page_length)

    def response_data(self):
        return {
            'cur_page': self.page_number,
            'total_page': self.paginator.num_pages,
            'page_length': self.page_length,
            'count': self.paginator.count,
            'data': self.page_object()
        }

    def serialized_data(self, serializer_class, context=None):
        ser = serializer_class(self.page_object(), many=True, context=context)
        return {
            'cur_page': self.page_number,
            'total_page': self.paginator.num_pages,
            'page_length': self.page_length,
            'count': self.paginator.count,
            'data': ser.data
        }

    def page_object(self, page_number=None):
        if page_number is None:
            page_number = self.page_number
        try:
            return self.paginator.page(page_number).object_list
        except EmptyPage:
            return list()
