import logging
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import RegisterSerializer, UsersListSerializer, UserSerializer
from .utils import generate_and_send_otp, set_cache_otp, verify_otp, delete_cache
from common.pagination import CustomPageNumberPagination
from common.exception_handlers import handle_unexpected_error
from .services.services import take_user_action, get_all_profiles

logger = logging.getLogger(__name__)

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
    
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class AdminUserListView(ListAPIView):
    queryset = get_all_profiles()
    serializer_class = UsersListSerializer
    permission_classes = [IsAdminUser]
    pagination_class =  CustomPageNumberPagination

class AdminUserActionView(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, pk):
        try:
            is_active = request.data.get("is_active", True)
            user_after_action = take_user_action(pk, is_active)
            serializer = UsersListSerializer(user_after_action)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            error = {"detail": "User with the given ID does not exist."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return handle_unexpected_error(err, "An unexpected error occured during user action.")
