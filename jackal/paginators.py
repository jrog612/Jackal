from django.core.paginator import EmptyPage, Paginator

from jackal.settings import jackal_settings


class JackalPaginator:
    def __init__(self, queryset, page_number=None, page_length=None):
        self.page_number = int(page_number) if page_number is not None else 1
        self.page_length = int(page_length) if page_length is not None else jackal_settings.PAGE_LENGTH
        self.paginator = Paginator(queryset, self.page_length)

    def response_data(self):
        return {
            'current_page': self.page_number,
            'total_page': self.paginator.num_pages,
            'page_length': self.page_length,
            'count': self.paginator.count,
            'data': self.page_object()
        }

    def serialized_data(self, serializer_class, context=None):
        ser = serializer_class(self.page_object(), many=True, context=context)
        return ser.data

    def meta_data(self):
        return {
            'current_page': self.page_number,
            'total_page': self.paginator.num_pages,
            'page_length': self.page_length,
            'count': self.paginator.count,
        }

    def page_object(self, page_number=None):
        if page_number is None:
            page_number = self.page_number
        try:
            return self.paginator.page(page_number).object_list
        except EmptyPage:
            return list()
