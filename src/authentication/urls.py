from django.urls import path

from authentication.api import _TokenObtainPairView, _TokenRefreshView

urlpatterns = [
    path("token/", _TokenObtainPairView.as_view()),
    path("token/refresh/", _TokenRefreshView.as_view()),
]
