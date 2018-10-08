from django.core.paginator import EmptyPage, Paginator


class JackalPaginator:
    def __init__(self, queryset, page_number, page_length):
        self.paginator = Paginator(queryset, page_length)
        self.page_number = int(page_number)
        self.page_length = int(page_length)

    @property
    def response_data(self):
        return {
            'cur_page': self.page_number,
            'total_page': self.paginator.num_pages,
            'page_length': self.page_length,
            'count': self.paginator.count,
            'data': self.page_object(),
        }

    def page_object(self, page_number=None):
        if page_number is None:
            page_number = self.page_number
        try:
            return self.paginator.page(page_number).object_list
        except EmptyPage:
            return list()


class SerializerPaginator(JackalPaginator):
    def __init__(self, queryset, serializer_class, page_number, page_length):
        self.serializer_class = serializer_class
        super().__init__(queryset, page_number, page_length)

    def page_object(self, page_number=None):
        paginate_data = super().page_object(page_number)
        return self.serializer_class(paginate_data, many=True).data
