from rest_framework.response import Response


class ResponseSimplizer:
    def success(self, detail='success', **kwargs):
        return Response({'detail': detail, **kwargs})

    def simple_response(self, result=None, status=200, headers=None, **kwargs):
        return Response(result, status=status, headers=headers, **kwargs)

    def bad_request(self, data):
        return Response(data, status=400)

    def forbidden(self, data):
        return Response(data, status=403)

    def internal_server_error(self, data):
        return Response(data, status=500)
