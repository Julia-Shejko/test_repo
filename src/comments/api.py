from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView

from comments.models import Comment
from comments.serializers import CommentSerializer
from tickets.models import Ticket
from users.constants import Role


class CommentsCreateAPI(CreateAPIView):
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]
        return Comment.objects.filter(ticket_id=ticket_id)


class CommentsListAPI(ListAPIView):
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"

    def __get_tickets(self):
        # The OR SQL processing
        # from django.db.models import Q
        # tickets = Ticket.objects.filter(
        #     Q(manager=self.request.user) | Q(customer=self.request.user)
        # )

        role: Role = self.request.user.role

        if role == Role.ADMIN:
            return Ticket.objects.all()
        elif role == Role.MANAGER:
            return Ticket.objects.filter(manager=self.request.user)

        return Ticket.objects.filter(customer=self.request.user)

    def get_queryset(self):
        tickets = self.__get_tickets()
        ticket = get_object_or_404(
            tickets,
            id=self.kwargs[self.lookup_field],
        )
        comments = ticket.comments.order_by("-created_at")

        return comments
