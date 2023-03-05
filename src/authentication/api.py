from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError  # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # type: ignore

from shared.serializers import ResponseSerializer


class _TokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = ResponseSerializer({"result": serializer.validated_data})

        return Response(response.data, status=status.HTTP_200_OK)


class _TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = ResponseSerializer({"result": serializer.validated_data})

        return Response(response.data, status=status.HTTP_200_OK)
