from django.apps import apps

from exceptions import FieldException

none_values = [[], {}, '', 'null', None, 'undefined']


def get_object_or_None(model, **fields):
    items = model.objects.filter(**fields)
    return items.first() if items.exists() else None


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
