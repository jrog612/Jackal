from jackal.exceptions import NotFound
from jackal.helpers.data_helper import isiter
from jackal.loaders import query_function_loader
from jackal.shortcuts import gen_q


class JackalQueryFilter:
    def __init__(self, queryset, params=None):
        self.queryset = queryset
        self.params = params or {}

    @staticmethod
    def _get_query_function(key):
        for n, callback in query_function_loader().items():
            if key.find(n) >= 0:
                return key.replace('__{}'.format(n), ''), callback
        else:
            return key, None

    def filter_map(self, filter_map):
        """
        params = {
            'name': 'Yongjin',
            'age_lowest': '20',
            'skills': 'django,python',
            'status[]': [1, 2, 3],
        }
        f = JackalQueryFilter(User.objects.all(), params)

        queryset = f.filter_map({
            'name': 'name__contains',
            'age_lowest': 'age__gte',
            'skills__to_list': 'skills__in',
            'status[]': 'status__in',
        }).queryset
        """

        queryset = self.queryset
        # initial
        filterable = {}
        filterable_q_objects = list()

        for map_key, filter_keyword in filter_map.items():
            # eg) map_key       : 'skills__to_list'
            #     filter_keyword: 'skills__in'
            map_key, callback = self._get_query_function(map_key)
            # eg) map_key  : skills
            #     call_back: to_list function at DefaultQueryFunction
            if map_key.find('[]') > 0 and hasattr(self.params, 'getlist'):  # django drf query_params getlist support
                param_value = self.params.getlist(map_key)
                if param_value in [None, '', []]:
                    continue  # if empty, skip
            else:
                param_value = self.params.get(map_key)
            # eg) param_value  : 'django,python'

            if param_value in [None, '']:
                continue
            elif callback is not None:
                param_value = callback(param_value)
                # eg) param_value  : ['django', 'python']

            if isiter(filter_keyword):  # if filter_keyword is such like ('name__contains', 'job__contains').
                # make Q object like Q(Q(name__contains={param_value}) | Q(job__contains={param_value}))
                filterable_q_objects.append(gen_q(param_value, *filter_keyword))
            else:
                filterable[filter_keyword] = param_value

        self.queryset = queryset.filter(**filterable).filter(*filterable_q_objects)
        return self

    def search(self, search_dict, search_keyword_key='search_keyword', search_type_key='search_type'):
        """
        params = {
            'search_keyword': 'Yongjin',
            'search_type': 'name',
        }
        f = JackalQueryFilter(User.objects.all(), params)

        queryset = f.search({
            'all': ('name__contains', 'job__contains', 'city__contains),
            'name': 'name__contains',
            'job': 'job__contains',
            'city': 'city__contains',
        }).queryset
        """

        queryset = self.queryset

        search_keyword = self.params.get(search_keyword_key)
        # if search_type is not exists, consider all type.
        search_type = self.params.get(search_type_key, 'all')
        # get search_type
        dict_value = search_dict.get(search_type, None)

        if dict_value is not None and search_keyword is not None:
            if isiter(dict_value):
                self.queryset = queryset.filter(gen_q(search_keyword, *dict_value))
            else:
                self.queryset = queryset.filter(**{dict_value: search_keyword})
        return self

    def extra(self, **extra_kwargs):
        """
        f = JackalQueryFilter(User.objects.all(), {})
        queryset = f.extra(age__lte=30, is_active=True).queryset
        """

        queryset = self.queryset
        self.queryset = queryset.filter(**extra_kwargs)
        return self

    def ordering(self, ordering_key='ordering'):
        """
        params = {
            'ordering': 'name,-age',
        }
        f = JackalQueryFilter(User.objects.all(), params)

        queryset = f.ordering().queryset
        """

        ordering = self.params.get(ordering_key)
        if ordering:
            queryset = self.queryset
            order_by = ordering.split(',')
            self.queryset = queryset.order_by(*order_by)
        return self

    def get(self, raise_404=False, **kwargs):
        """
        f = JackalQueryFilter(User.objects.all(), {})
        user = f.get(id=5)
        """
        queryset = self.queryset
        obj = self.queryset.filter(**kwargs).first()
        if obj is None and raise_404:
            raise NotFound(model=queryset.model, filters=kwargs)

        return obj
