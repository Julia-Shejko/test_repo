from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.serializers import ResponseMultiSerializer, ResponseSerializer
from tickets.models import Ticket
from tickets.permissions import RoleIsAdmin, RoleIsManager, RoleIsUser, TicketManager, TicketOwner
from tickets.serializers import TicketLightSerializer, TicketSerializer
from users.constants import Role


class TicketAPISet(ModelViewSet):
    queryset = Ticket.objects.all()
    model = Ticket
    serializer_class = TicketSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [RoleIsUser]
        elif self.action == "update":
            permission_classes = [RoleIsAdmin | TicketManager]
        elif self.action == "list":
            permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
        elif self.action == "retrieve":
            permission_classes = [RoleIsAdmin | TicketManager | TicketOwner]
        elif self.action == "destroy":
            permission_classes = [RoleIsAdmin | TicketManager]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def create(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        context: dict = {"request": self.request}

        serializer = TicketSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = ResponseSerializer({"result": serializer.data})

        return Response(response.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        instance: Ticket = self.get_object()

        context: dict = {"request": self.request}
        serializer = TicketSerializer(
            instance=instance,
            data=request.data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = ResponseSerializer({"result": serializer.data})

        return Response(response.data, status=status.HTTP_201_CREATED)

    def list(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        if request.user.role == Role.ADMIN:  # type: ignore
            queryset = self.get_queryset()
        elif request.user.role == Role.MANAGER:  # type: ignore
            queryset = Ticket.objects.filter(manager=request.user)  # type: ignore
        else:
            queryset = Ticket.objects.filter(customer=request.user)  # type: ignore

        serializer = TicketLightSerializer(queryset, many=True)
        response = ResponseMultiSerializer({"results": serializer.data})

        return Response(response.data)

    def retrieve(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        instance: Ticket = self.get_object()

        serializer = TicketSerializer(instance)
        response = ResponseSerializer({"result": serializer.data})

        return Response(response.data)

    def destroy(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        instance: Ticket = self.get_object()
        instance.delete()

        return Response({"result": "The ticket has been deleted"}, status=status.HTTP_204_NO_CONTENT)
