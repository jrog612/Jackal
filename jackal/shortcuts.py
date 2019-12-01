from django.apps import apps
from django.db import models
from django.db.models import Q
from django.shortcuts import _get_queryset

from jackal.exceptions import NotFound
from jackal.loaders import structure_loader
from jackal.settings import jackal_settings


def get_object_or_None(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_object_or(klass, this=None, *args, **kwargs):
    return get_object_or_None(klass, *args, **kwargs) or this


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


def get_model(*args, **kwargs):
    return apps.get_model(*args, **kwargs)


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


def status_readable(status, key):
    stru = structure_loader('STATUS_READABLE_CLASSES').get(key, {})
    return stru.get(status, jackal_settings.UNKNOWN_READABLE)


def gen_q(key, *filter_keywords):
    q_object = Q()
    for q in filter_keywords:
        q_object |= Q(**{q: key})
    return q_object


def fk_filter(**kwargs):
    result = {}
    for key, value in kwargs.items():
        if type(value) is int or type(value) is str:
            result['{}_id'.format(key)] = int(value)
        elif isinstance(value, models.Model):
            result[key] = value
        else:
            raise ValueError('{} is invalid value for django filtering'.format(type(value)))
    return result
