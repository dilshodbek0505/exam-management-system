from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializes import UserSeriaizer, LoginSerializer
from apps.user.tasks import send_verification_email
from apps.user.utils import verify_url



class RegisterApi(CreateAPIView):
    serializer_class = UserSeriaizer
    
    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email.delay(user.id)


class VerificationEmailApi(APIView):
    def get(self, request, url, *args, **kwargs):
        verify_url(url)
        return Response({'success'}, status=200)


class LoginApi(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, requets, *args, **kwargs):
        serializer = self.serializer_class(data = requets.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)
        
        
__all__ = [
    'RegisterApi',
    'VerificationEmailApi',
    'LoginApi',
]