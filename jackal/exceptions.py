from rest_framework.response import Response
from rest_framework.views import exception_handler

from base import JackalAPIException


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
        filter_message = ', '.join([f'{key}={value}' for key, value in self.filters.items()])
        return '{}에서 {} 조건에 해당하는 항목을 찾을 수 없습니다.'.format(self.model.__name__, filter_message)

    def response_data(self):
        return {'message': self.message, 'model': self.model.__name__}


class ForbiddenException(MessageException):
    status_code = 403


class BadRequestException(MessageException):
    status_code = 400


class AlreadyExistException(MessageException):
    default_message = '이미 존재하는 데이터입니다.'
    status_code = 400


class ErrorCodeException(JackalAPIException):
    status_code = 400

    def __init__(self, code, message, **kwargs):
        self.code = code
        self.message = message
        self.kwargs = kwargs

    def response_data(self):
        return {
            'message': self.message,
            'code': self.code,
        }


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


def jackal_exception_handler(exc, context):
    if isinstance(exc, JackalAPIException):
        return Response(exc.response_data(), status=exc.status_code)
    else:
        return exception_handler(exc, context)
