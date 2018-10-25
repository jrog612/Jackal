from django.apps import apps

from jackal.exceptions import FieldException, NotFoundException, StructureException
from jackal.loaders import structure_loader

none_values = [[], {}, '', 'null', None, 'undefined']


def get_object_or_None(model, **fields):
    items = model.objects.filter(**fields)
    return items.first() if items.exists() else None


def get_object_or_404(model, **fields):
    obj = get_object_or_None(model, **fields)
    if obj is None:
        raise NotFoundException(model, fields)
    return obj


def model_update(instance, **fields):
    for key, value in fields.items():
        setattr(instance, key, value)

    instance.save()
    return instance


def get_model(model_name):
    return apps.get_model(model_name)


def remove_unexpected(data, expected):
    """
    기대하지 않은 값들 모두 제외
    """
    expected_dict = {key: value for key, value in data.items() if key in expected}
    return expected_dict


def check_required(data, required):
    """
    필수값 체크용 함수
    """
    if required == '*':
        required = data.keys()

    for req in required:
        if data.get(req) in none_values:
            raise FieldException(field=req, message='Required')
    return True


def change_None(data, fields=None):
    """
    None, '', 'null', 'undefined' 를 모두 None 으로 변환하는 함수. fields 를 주면 해당 fields 내에 있는 것들만 변환합니다.
    """
    copied_data = data.copy()
    if fields == '*':
        fields = None

    for key, value in data.items():
        if value in none_values:
            if fields is None:
                copied_data[key] = None
            elif key in fields:
                copied_data[key] = None
    return copied_data


def remove_None(data, fields=None):
    """
    None, '', 'null', 'undefined' 를 모두 제외합니다. fields 를 주면 해당 fields 만 검사합니다.
    """
    copied_data = data.copy()
    if fields == '*':
        fields = None

    for key, value in data.items():
        if value in none_values:
            if fields is None:
                copied_data.pop(key)
            elif key in fields:
                copied_data.pop(key)
    return copied_data


def inspect_data(data, key):
    try:
        valid_structure = structure_loader('INSPECT_CLASSES')[key]
    except KeyError:
        raise StructureException('no valid structure about {} key'.format(key))

    filtered = data

    # 예상하지 못한 필드들은 제외
    expected = valid_structure.get('expected', None)
    if expected is not None:
        filtered = remove_unexpected(data, expected)

    # 필수 값 체크
    required = valid_structure.get('required', None)
    if required is not None:
        check_required(filtered, required=required)

    # 공백을 허용하지 않는 값 None 처리
    null_array = valid_structure.get('null', None)
    if null_array is not None:
        filtered = change_None(filtered, valid_structure['null'])

    # 디폴드 값이 있어서 빈 값이나 None 을 허용하지 않는 필드 제외
    default_array = valid_structure.get('default', None)
    if default_array is not None:
        filtered = remove_None(filtered, valid_structure['default'])

    return filtered


def status_setter(obj, status, key, commit=True, status_field='status'):
    if not status_checker(status, obj.status, key):
        return False

    setattr(obj, status_field, status)

    if commit:
        obj.save()
    return True


def operating(a, oper, b):
    if oper == '==':
        return a == b
    elif oper == '<=':
        return a <= b
    elif oper == '<':
        return a < b
    elif oper == '>=':
        return a >= b
    elif oper == '>':
        return a > b
    elif oper == '!=':
        return a != b
    else:
        return False


def status_checker(change_to, current, key):
    stru = structure_loader('STATUS_CONDITION_CLASSES').get(key)
    if stru is None:
        return False

    condition = stru.get(change_to)

    if condition is None:
        return False

    for operator, target_status in condition:
        if not operating(current, operator, target_status):
            return False

    return True


def readable_status(key, status):
    stru = structure_loader('STATUS_READABLE_CLASSES').get(key)
    if stru is None:
        return '알 수 없음'

    return stru.get(status, '알 수 없음')
