from django.shortcuts import render

# Create your views here.
class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class= RegistrationSerializer
    
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OAuthAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = OAuthSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = OAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendEmailOTP(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendEmailOTPSerializer
    
    
    
class VerifyEmailOTP(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailOTPSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class SendPhoneOTP(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendPhoneOTPSerializer
    
    def create(self, request, *args, **kwargs):
        response = super(SendPhoneOTP, self).create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response