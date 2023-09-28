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
