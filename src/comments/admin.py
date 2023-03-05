from django.contrib import admin

from comments.models import Comment
from shared.django import TimeStampReadonlyAdmin


@admin.register(Comment)
class CommentsAdmin(TimeStampReadonlyAdmin):
    list_display = ["body", "ticket", "user"]
    search_fields = ["body", "ticket__header"]
