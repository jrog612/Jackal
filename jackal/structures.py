class JackalBaseStructure:
    prefix = 'structure'

    @classmethod
    def get_structure(cls):
        """
        정의된 prefix 값을 이용하여 해당 클래스 내의 {prefix}_ 형태로 시작하는 모든 항목들을 가져옵니다.
        만약 항목이 함수라면, 해당 함수를 실행한 값을 최종 딕셔너리에 업데이트하고, 일반 딕셔너리라면 바로 업데이트합니다.
        사전도, 함수도 아니라면 건너 뜁니다.
        """
        ret_dict = {}
        for key in cls.__dict__.keys():
            if key.find('{}_'.format(cls.prefix)) == 0:
                value = getattr(cls, key, {})
                if callable(value):
                    ret_dict.update(value())
                elif type(value) is dict:
                    ret_dict.update(value)
                else:
                    continue

        return ret_dict


class BaseStatusCondition(JackalBaseStructure):
    """
    StatusCondition 는 시스템 로직에서 필요한 다양한 상태 값의 변경에 대한 조건 체크를 용의하게 해주는 구조체입니다.

    어떤 한 상태에서 다른 상태로 변경되기 위해 번거로운 처리들을 매번 하기는 성가십니다. 상태를 체크하는 함수를 만들더라도, 상태가 사용되는
    객체마다 모두 상태 체크 함수를 만들어줘야 하죠.

    StatusCondition 를 이용하여 상태 변경의 조건들을 정의해두면, jackal 의 shortcut 함수 중 하나인 status_checker 를 이용하여
    그 어떤 객체의 상태건 모두 한번에 체크가 가능해 집니다.

    해당 클래스를 상속받은 뒤, JACKAL_SETTINGS 내의 STATUS_CONDITION_CLASSES 에 클래스의 경로를 추가하면, 등록이 완료됩니다.

    ex)
    order_status = {
        'wait': '주문이 막 접수되어 상품 준비 대기 중인 상태입니다.',
        'ready': '상품이 준비 되었습니다.',
        'delivering': '배송중입니다.',
        'delivered': '배송이 완료되었습니다.',
        'cancel': '주문이 취소되었습니다.',
    }
    order_status_int = {
        'wait': 0,
        'ready': 1,
        'delivering': 2,
        'delivered': 3,
        'cancel': 99,
    }

    MyStatusCondition(BaseStatusCondition):
        prefix = 'status'

        status_order = {
            'order_ver_str': {
                'ready': (
                    # 대기 중일 때만 상품 준비 상태로 변경 가능합니다.
                    ('==', 'wait'),
                ),
                'delivering': (
                    # 상품이 준비되어있거나, 준비 대기중일 때만 배송중으로 변경이 가능합니다.
                    ('==', 'wait'), ('==', 'ready')
                ),
                'delivered': (
                    ('==', 'delivering'), ('==', 'ready'), ('==', 'wait')
                ),
                'cancel': (
                    # 상품이 배송되기 전에만 취소가 가능합니다.
                    ('==', 'wait'), ('==', 'ready')
                )
            },
            # 숫자를 이용할 경우 더 많은 비교 연산자를 이용할 수 있습니다.
            'order_ver_int': {
                order_status_int['ready']: (
                    ('==', order_status_int['wait']),
                ),
                'delivering': (
                    ('<=', order_status_int['ready']),
                ),
                'delivered': (
                    ('<=', order_status_int['delivering']),
                ),
                'cancel': (
                    ('<', order_status_int['delivering']),
                )
            }
        }

    print(status_checker(change_to='ready', current='wait', key='order_ver_str'))
    >> True
    """
    pass


class BaseStatusReadable(JackalBaseStructure):
    """
    Status Readable 은 데이터 상으로 판별하는 상태 값을 사용자에게 직접 노출하기 위해서 readable 한 문자 값으로 변경할 때 사용되는
    상태: 사용자표시값 매핑 구조체입니다.

    jackal 의 readable_status shortcut 을 이용하여 정의한 구조체에서 손쉽게 사용자 표시용 상태 문자열을 불러오십시오.

    해당 클래스를 상속받은 뒤, JACKAL_SETTINGS 내의 STATUS_READABLE_CLASSES 에 클래스의 경로를 추가하면, 등록이 완료됩니다.

    ex)
    MyStatusReadable(BaseStatusCondition):
        prefix = 'status'

        status_order = {
            'order': {
                'wait': '상품준비중',
                'ready': '상품준비완료',
                'delivering': '배송중',
                'delivered': ''배송완료',
                'cancel': '주문취소'
            },
        }

    print(readable_status(order.status, 'order'))
    >> '배송완료'
    """
    pass


class BaseQueryFunction:
    """
    RequestFilter 에서 사용하게 될, 쿼리 함수들을 정의할 수 있는 클래스입니다.

    해당 클래스를 상속받고, JACKAL_SETTINGS 내의 QUERY_FUNCTION_CLASSES 에 정의한 클래스의 경로를 추가하는 것으로 등록이 완료됩니다.

    등록한 쿼리 함수들은 filter_map 내에서 사용 가능하게 됩니다.

    ex)

    class MyQueryFunction(BaseQueryFunction):
        prefix = 'func' # you can customize

        @staticmethod
        def func_to_list(data):
            return data.split(',')

        @staticmethod
        def func_to_boolean(data):
            return data.lower() == 'true'


    filter_map = {
        # this will change to is_active. and value will change True or False
        'is_active__to_boolean': 'is_active',
        # string will split by comma and change to tags
        'tags__to_list': 'tag__in'
    }
    """

    prefix = 'func'

    @classmethod
    def get_function_set(cls):
        ret_dict = {}

        for name, func in cls.__dict__.items():
            if name.find('{}_'.format(cls.prefix)) == 0:
                name = name.replace('{}_'.format(cls.prefix))
                ret_dict[name] = func
        return ret_dict


class DefaultQueryFunction(BaseQueryFunction):
    @staticmethod
    def func_to_list(data):
        return data.split(',')

    @staticmethod
    def func_to_boolean(data):
        return data.lower() == 'true'
