from django.urls import path

from tests.test_apiviews.test_extra import GetterResponseTestAPIView
from tests.test_apiviews.test_filtering import FilteringTestAPI
from tests.test_apiviews.test_pre_post import PrePostTestAPI
from tests.test_exceptions import TestExceptionAPI

urlpatterns = [
    path('extra', GetterResponseTestAPIView.as_view()),
    path('exception', TestExceptionAPI.as_view()),
    path('filtering', FilteringTestAPI.as_view()),
    path('pre-post/<str:kind>', PrePostTestAPI.as_view())
]
