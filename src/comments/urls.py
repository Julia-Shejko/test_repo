from django.urls import path

from comments.api import CommentsCreateAPI, CommentsListAPI

# In this application we didn't follow the HTTP approach
# in order to have 2 different approaches in this project

urlpatterns = [
    path(
        "tickets/<int:ticket_id>/comments/create",
        CommentsCreateAPI.as_view(),
    ),
    path(
        "tickets/<int:ticket_id>/comments",
        CommentsListAPI.as_view(),
    ),
]
