from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.serializers import ResponseMultiSerializer, ResponseSerializer
from users.constants import Role
from users.permissions import AccountOwner, RoleIsAdmin
from users.serializers import UserLightSerializer, UserRegistrationSerializer, UserSerializer, UserUpdateSerializer

User = get_user_model()


class UserAPISet(ModelViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer
    lookup_field = "pk"

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "update":
            permission_classes = [RoleIsAdmin | AccountOwner]
        elif self.action == "list":
            permission_classes = [RoleIsAdmin]
        elif self.action == "retrieve":
            permission_classes = [RoleIsAdmin | AccountOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def _get_queryset(self):
        role: Role = self.request.user.role

        if role == Role.ADMIN:
            return User.objects.all()
        else:
            user = User.objects.filter(email=self.request.user.email)
            return get_object_or_404(user, id=self.kwargs[self.lookup_field])

    def create(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        context: dict = {"request": self.request}

        serializer = UserRegistrationSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = ResponseSerializer({"result": serializer.data})

        return Response(response.data, status=status.HTTP_201_CREATED)

    def list(self, request: Request | Request, *args, **kwargs) -> Response | Response:

        queryset = User.objects.all()

        serializer = UserLightSerializer(queryset, many=True)
        response = ResponseMultiSerializer({"results": serializer.data})

        return Response(response.data)

    def retrieve(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        if request.user.role == Role.ADMIN:  # type: ignore
            users = User.objects.all()
            instance = get_object_or_404(users, id=self.kwargs[self.lookup_field])
        else:
            user = User.objects.filter(email=self.request.user.email)  # type: ignore
            instance = get_object_or_404(user, id=self.kwargs[self.lookup_field])

        serializer = UserSerializer(instance)
        response = ResponseSerializer({"result": serializer.data})

        return Response(response.data)

    def update(self, request: Request | Request, *args, **kwargs) -> Response | Response:
        instance = self._get_queryset()
        context: dict = {"request": self.request}

        serializer = UserUpdateSerializer(instance, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = ResponseSerializer({"result": serializer.data})

        return Response(response.data, status=status.HTTP_201_CREATED)
