from django.urls import path

from tests.test_apiviews.test_extra import GetterResponseTestAPIView
from tests.test_exceptions import TestExceptionAPI

urlpatterns = [
    path('extra', GetterResponseTestAPIView.as_view()),
    path('exception', TestExceptionAPI.as_view()),
]
