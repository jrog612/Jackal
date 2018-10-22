from django.core.paginator import EmptyPage, Paginator


class JackalPaginator:
    def __init__(self, queryset, request, default_page=1, default_limit=10):
        page = request.query_params.get('page_number', default_page)
        if int(page) <= 0:
            page = 1
        limit = request.query_params.get('page_length', default_limit)

        self.paginator = Paginator(queryset, limit)
        self.page_number = int(page)
        self.page_length = int(limit)

    def response_data(self):
        return {
            'cur_page': self.page_number,
            'total_page': self.paginator.num_pages,
            'page_length': self.page_length,
            'count': self.paginator.count,
            'data': self.page_object()
        }

    def serialized_data(self, serializer_class, context=None):
        data = serializer_class(self.page_object(), many=True, context=context)
        return {
            'cur_page': self.page_number,
            'total_page': self.paginator.num_pages,
            'page_length': self.page_length,
            'count': self.paginator.count,
            'data': data
        }

    def page_object(self, page_number=None):
        if page_number is None:
            page_number = self.page_number
        try:
            return self.paginator.page(page_number).object_list
        except EmptyPage:
            return list()
