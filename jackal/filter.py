from django.db.models import Q


class RequestQueryFilter:
    def __init__(self, queryset, query_param, filter_map, search_type=None):
        self.queryset = queryset
        self.query_param = query_param
        self.filter_map = filter_map
        self.search_type = search_type

    @property
    def data(self):
        self.queryset = self.filtering_with_filter_map()

        if self.query_param.get('ordering'):
            self.queryset = self.ordering()

        return self.queryset

    def filtering_with_filter_map(self):
        filterable = {}
        # 복합 쿼리를 위한 Q 오브첵트 리스트를 미리 정의한다.
        q_objects = list()

        # search_type 과 그에 해당하는 타입 실제 값을 가져온다.
        search_type_value = self.query_param.get('search_type', None)

        queryset = self.queryset

        for map_key, filter_keyword in self.filter_map.items():
            # filter_map 내에 있는 key 즉, map_key 의 이름에서 __to_boolean 과 같은 확장 함수가 사용됐는지 체크한다.
            map_key, callback = self.get_key_function(map_key)
            # 필터링을 위해 map_key 에 매칭되는 값을 get 파라미터 내에서 가져온다.
            key = self.query_param.get(map_key)

            # map_key 가 search_keyword 고 type_dict 가 None 이 아니고, value 도 존재한다면.
            if map_key == 'search_keyword' and self.search_type is not None and search_type_value:
                # filter_keyword 를 type_dict 내에 있는 값으로 변환시켜버린다.
                type_val = self.search_type.get(search_type_value)
                if type_val is not None:
                    filter_keyword = type_val

            # 값이 비어있거나, 없으면 건너뛰기
            if key in [None, ''] or map_key == 'search_type':
                continue

            # __function 형태의 map_key 인지 체크하여 callback 함수를 가져옴.
            if callback is not None:
                key = callback(key)

            # 복합 쿼리일 시에 q 오브젝트로 or 연산을 진행 할 수 있게 한다.
            if type(filter_keyword) == tuple:
                q_objects.append(self.get_q_object(key, *filter_keyword))
            # 아닐 경우 일반 키워드 등록으로 and 연산을 진행할 수 있게 한다.
            else:
                filterable[filter_keyword] = key

        # 최종적으로 필터를 적용시킨다.
        return queryset.filter(*q_objects, **filterable).distinct()

    def ordering(self):
        order_by = self.query_param.get('ordering').split(',')

        return self.queryset.order_by(*order_by)

    def get_q_object(self, key, *filter_keywords):
        q_object = Q()
        for q in filter_keywords:
            q_object |= Q(**{q: key})
        return q_object

    def get_key_function(self, key):
        for func_set_key, callback in QueryFunc.func_set().items():
            if key.find(func_set_key) >= 0:
                return key.replace(func_set_key, ''), callback
        else:
            return key, None


class QueryFunc:
    @staticmethod
    def func_set():
        return {
            '__to_list'   : QueryFunc.to_list,
            '__to_boolean': QueryFunc.to_boolean,
        }

    @staticmethod
    def to_list(data):
        return data.split(',')

    @staticmethod
    def to_boolean(data):
        return data.lower() == 'true'
