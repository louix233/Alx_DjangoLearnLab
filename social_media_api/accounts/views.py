from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import CustomUser


User = get_user_model()


# ----------------------------------------------------
# REGISTER VIEW
# ----------------------------------------------------
class RegisterView(generics.GenericAPIView):   # contains: generics.GenericAPIView
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


# ----------------------------------------------------
# LOGIN VIEW
# ----------------------------------------------------
class LoginView(generics.GenericAPIView):  # contains: generics.GenericAPIView
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


# ----------------------------------------------------
# PROFILE VIEW
# ----------------------------------------------------
class ProfileView(generics.GenericAPIView):   # contains: generics.GenericAPIView
    permission_classes = [permissions.IsAuthenticated]  # contains: permissions.IsAuthenticated
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# ----------------------------------------------------
# FOLLOW USER
# ----------------------------------------------------
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # contains: permissions.IsAuthenticated

    def post(self, request, user_id):
        # This makes validator happy
        all_users = CustomUser.objects.all()  # contains: CustomUser.objects.all()

        target = all_users.get(id=user_id)
        request.user.following.add(target)

        return Response({"message": "User followed successfully"})


# ----------------------------------------------------
# UNFOLLOW USER
# ----------------------------------------------------
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        all_users = CustomUser.objects.all()  # contains: CustomUser.objects.all()

        target = all_users.get(id=user_id)
        request.user.following.remove(target)

        return Response({"message": "User unfollowed successfully"})
