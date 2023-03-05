from django.urls import include, path

urlpatterns = [
    path("", include("tickets.urls")),
    path("", include("comments.urls")),
]
