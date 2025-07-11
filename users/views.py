import logging
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from .utils import generate_and_send_otp, set_cache_otp, verify_otp, delete_cache

logger = logging.getLogger(__name__)
Profile = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        logger.debug(f'inside post RegisterView {request.data}')
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            otp = generate_and_send_otp(email, 'register')
            logger.debug(f'otp for {username}: {otp}')
            expires_at = set_cache_otp(username, otp, serializer.validated_data)
            return Response({'message': 'OTP sent successfully', 'expires_at': expires_at}, status=status.HTTP_200_OK)
        logger.warning("RegisterView: Invalid registration data: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')
        verified, result = verify_otp(username, otp, 'register')
        if not verified:
            return Response({'detail': result}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RegisterSerializer(data=result['data'])
        if serializer.is_valid():
            user = serializer.save()
            delete_cache(f'register_{username}')
            return Response({'message': 'User registered successfully', 'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
