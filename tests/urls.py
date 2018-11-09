from django.urls import path

from tests.test_apiviews.test_extra import GetterResponseTestAPIView

urlpatterns = [
    path('extra', GetterResponseTestAPIView.as_view()),
]
