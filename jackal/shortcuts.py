import collections

import six
from django.apps import apps

from jackal.exceptions import NotFound
from jackal.loaders import structure_loader


def iterable(arg):
    return isinstance(arg, collections.Iterable) and not isinstance(arg, six.string_types)


def get_object_or_None(model, **fields):
    items = model.objects.filter(**fields)
    return items.first() if items.exists() else None


def get_object_or_404(model, **fields):
    obj = get_object_or_None(model, **fields)
    if obj is None:
        raise NotFound(model, fields)
    return obj


def model_update(instance, **fields):
    for key, value in fields.items():
        setattr(instance, key, value)

    instance.save()
    return instance


def get_model(model_name):
    return apps.get_model(model_name)


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
