from rest_framework.response import Response

from jackal.base import JackalAPIException


class MessageException(JackalAPIException):
    default_message = ''

    def __init__(self, message=None, **kwargs):
        if message is None:
            self.message = self.default_message
        else:
            self.message = message
        self.kwargs = kwargs

    def response_data(self):
        return {'message': self.message, **self.kwargs}


class NotFoundException(MessageException):
    status_code = 404

    def __init__(self, model, **filters):
        self.model = model
        self.filters = filters

    @property
    def message(self):
        filter_condition = ', '.join([f'{key}={value}' for key, value in self.filters.items()])
        return 'can not find {} model about \'{}\' condition'.format(self.model.__name__, filter_condition)

    def response_data(self):
        return {'message': self.message, 'model': self.model.__name__}


class ForbiddenException(MessageException):
    status_code = 403


class BadRequestException(MessageException):
    status_code = 400


class AlreadyExistException(MessageException):
    default_message = 'data already exists'
    status_code = 400


class FieldException(JackalAPIException):
    status_code = 400

    def __init__(self, field, message, **kwargs):
        self.field = field
        self.message = message
        self.kwargs = kwargs

    def response_data(self):
        return {
            'message': self.message,
            'field': self.field,
        }


def jackal_exception_handler(exc):
    if isinstance(exc, JackalAPIException):
        return Response(exc.response_data(), status=exc.status_code)
    return None
