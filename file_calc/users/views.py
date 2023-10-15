from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import models, serializers


class UserRegisterAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = models.User.objects.all()
    serializer_class = serializers.UserRegisterSerializer


class UserLogIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token_key': token.key,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'contact_number': user.contact_number,
        })
