from functools import wraps


def return_mutable(mutable_type='dict'):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if mutable_type == 'dict':
                ret_data = dict()
            elif mutable_type == 'list':
                ret_data = list()
            elif mutable_type == 'set':
                ret_data = set()
            else:
                ret_data = None

            func(ret_data, *args, **kwargs)
            return ret_data

        return inner

    return decorator
