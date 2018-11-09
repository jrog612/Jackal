from django.urls import path

from tests.test_apiviews.test_getter import GetterTestAPIView

urlpatterns = [
    path('getter', GetterTestAPIView.as_view()),
]
