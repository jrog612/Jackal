from rest_framework import permissions

REAL_SAFE = ('OPTIONS', 'HEAD')
POST = 'POST'
GET = 'GET'
PATCH = 'PATCH'
PUT = 'PUT'
DELETE = 'DELETE'


class _HttpMethodPermission(permissions.BasePermission):
    allow_method = ''

    def has_permission(self, request, view):
        if request.method in REAL_SAFE:
            return True
        return request.method == self.allow_method

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsGet(_HttpMethodPermission):
    """
    GET 요청을 체크합니다.
    """
    allow_method = GET


class IsPost(_HttpMethodPermission):
    """
    POST 요청을 체크합니다.
    """
    allow_method = POST


class IsPut(_HttpMethodPermission):
    """
    PATCH 요청을 체크합니다.
    """
    allow_method = PUT


class IsPatch(_HttpMethodPermission):
    """
    PATCH 요청을 체크합니다.
    """
    allow_method = PATCH


class IsDelete(_HttpMethodPermission):
    """
    DELETE 요청을 체크합니다.
    """
    allow_method = DELETE


class HasAuth(permissions.IsAuthenticated):
    pass


class HasAuthOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass
