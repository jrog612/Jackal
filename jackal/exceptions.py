from rest_framework.exceptions import APIException
from rest_framework.response import Response


class JackalAPIException(APIException):
    default_message = ''
    status_code = None

    def __str__(self):
        return self.__class__.__name__

    def response_data(self):
        return {}


class MessageException(JackalAPIException):
    default_message = ''

    def __init__(self, message=None, context=None, **kwargs):
        self.message = message if message is not None else self.default_message
        self.context = context if context is not None else dict()
        self.kwargs = kwargs

    def response_data(self):
        return {'message': self.message, **self.kwargs}


class NotFound(MessageException):
    status_code = 404
    message_form = 'Can not find {} model instance filtered by \'{}\''

    def __init__(self, model, filters, context=None, **kwargs):
        self.model = model
        self.filters = filters
        self.context = context
        self.kwargs = kwargs

    @property
    def message(self):
        filter_condition = ', '.join(['{}={}'.format(key, value) for key, value in self.filters.items()])
        return self.message_form.format(self.model.__name__, filter_condition)

    def response_data(self):
        return {'message': self.message, 'model': self.model.__name__, **self.kwargs}


class Forbidden(MessageException):
    status_code = 403


class BadRequest(MessageException):
    status_code = 400


class FieldException(JackalAPIException):
    status_code = 400

    def __init__(self, field, message, context=None, **kwargs):
        self.field = field
        self.message = message
        self.kwargs = kwargs
        self.context = context if context is not None else dict()

    def response_data(self):
        return {
            'message': self.message,
            'field': self.field,
            **self.kwargs
        }


def jackal_exception_handler(exc, context):
    if isinstance(exc, JackalAPIException):
        return Response(exc.response_data(), status=exc.status_code)
    return None
