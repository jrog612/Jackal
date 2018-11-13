from jackal.exceptions import NotFound
from jackal.helpers.data_helper import isiter
from jackal.loaders import query_function_loader
from jackal.shortcuts import gen_q


class JackalQueryFilter:
    def __init__(self, queryset, params=None):
        self.queryset = queryset
        if params is None:
            params = {}
        self.params = params

    @staticmethod
    def _get_query_function(key):
        for n, callback in query_function_loader().items():
            if key.find(n) >= 0:
                return key.replace(n, ''), callback
        else:
            return key, None

    def filter_map(self, filter_map):
        """
        params = {
            'name': 'Yongjin',
            'age_lowest': '20',
        }
        f = JackalQueryFilter(User.objects.all(), params)

        queryset = f.filter_map({
            'name': 'name__contains',
            'age_lowest': 'age__gte'
        }).queryset
        """

        queryset = self.queryset

        filterable = {}
        filterable_q_objects = list()
        for map_key, filter_keyword in filter_map.items():
            map_key, callback = self._get_query_function(map_key)
            param_value = self.params.get(map_key)

            if param_value in [None, '']:
                continue
            elif callback is not None:
                param_value = callback(param_value)

            if isiter(filter_keyword):
                filterable_q_objects.append(gen_q(param_value, *filter_keyword))
            else:
                filterable[filter_keyword] = param_value

        self.queryset = queryset.filter(*filterable_q_objects, **filterable).distinct()
        return self

    def search(self, search_dict, search_keyword_key='search_keyword', search_type_key='search_type'):
        queryset = self.queryset

        search_keyword = self.params.get(search_keyword_key)
        search_type = self.params.get(search_type_key, 'all')

        dict_value = search_dict.get(search_type, None)

        if dict_value is not None and search_keyword is not None:
            if isiter(dict_value):
                self.queryset = queryset.filter(gen_q(search_keyword, *dict_value))
            else:
                self.queryset = queryset.filter(**{dict_value: search_keyword})
        return self

    def extra(self, **extra_kwargs):
        """
        """
        queryset = self.queryset
        self.queryset = queryset.filter(**extra_kwargs)
        return self

    def ordering(self, ordering_key='ordering'):
        """
        """
        ordering = self.params.get(ordering_key)
        if ordering:
            queryset = self.queryset
            order_by = ordering.split(',')
            self.queryset = queryset.order_by(*order_by)
        return self

    def get(self, raise_404=False, **kwargs):
        """
        """
        queryset = self.queryset
        obj = self.queryset.filter(**kwargs).first()
        if obj is None and raise_404:
            raise NotFound(model=queryset.model, filters=kwargs)

        return obj
