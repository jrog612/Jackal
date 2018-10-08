from django.core.paginator import EmptyPage, Paginator


class JackalPaginator:
    def __init__(self, queryset, serializer_class, page_number, page_length):
        self.paginator = Paginator(queryset, page_length)
        self.serializer_class = serializer_class
        self.page_number = int(page_number)
        self.page_length = int(page_length)

    @property
    def response_data(self):
        return {
            'cur_page'   : self.page_number,
            'total_page' : self.paginator.num_pages,
            'page_length': self.page_length,
            'count'      : self.paginator.count,
            'data'       : self.page_object(),
        }

    def page_object(self, page_number=None):
        if page_number is None:
            page_number = self.page_number
        try:
            paginate_data = self.paginator.page(page_number).object_list
        except EmptyPage:
            paginate_data = []

        return self.serializer_class(paginate_data, many=True).data
