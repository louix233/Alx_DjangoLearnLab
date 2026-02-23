from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CustomUser

@api_view(['POST'])
def register(request):
    user = CustomUser.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password']
    )
    token = Token.objects.create(user=user)
    return Response({"token": token.key})

@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )
    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})
