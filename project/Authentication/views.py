from django.shortcuts import render

# Create your views here.
class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class= RegistrationSerializer
    
