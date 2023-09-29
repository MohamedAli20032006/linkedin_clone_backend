from rest_framework import status
from rest_framework.generics import *
from Network.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import *
from Profile.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from datetime import datetime

class ConnectionRequestSendView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestSerializer
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user = self.request.user.id)
        return ConnectionRequest.objects.filter(sender = profile).exclude(state= "Withdrawn")

    def post(self, request, *args, **kwargs):
        
        sender_profile = get_object_or_404(Profile, user = self.request.user.id)
        request.data.update({"sender" : sender_profile.id})
        try:
            username = self.request.data['reciever']
        except KeyError :
            return super().post(request, *args, **kwargs)
        
        reciever_profile = get_object_or_404(Profile, username = username)
        request.data.update({"reciever" : reciever_profile.id})
        return super().post(request, *args, **kwargs)


class ConnectionRequestWithdrawView(UpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestWithdrawSerializer
    
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user = self.request.user.id)
        return ConnectionRequest.objects.filter(sender = profile).exclude(state= "Withdrawn")
   
    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return Response({"message": "Your sent request has been withdrawn successfully"},
                         status=status.HTTP_200_OK)
        
        
class ConnectionRequestReceiveView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestSerializer
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user = self.request.user.id)
        return ConnectionRequest.objects.filter(reciever = profile, state = "Pending") 
    

class ConnectionRequestIgnoreView(UpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestIgnoreSerializer
    
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user = self.request.user.id)
        return ConnectionRequest.objects.filter(reciever = profile, state = "Pending") 
    
    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return Response({"message": "The request received has been ignored successfully"},
                         status=status.HTTP_200_OK)        
        
        
class ConnectionRequestAcceptView(views.APIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestAcceptSerializer

    
    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context = self.request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConnectionRemoveView(views.APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self,request, *args, **kwargs):
        try:
            username = self.request.data['username']
            user1 = self.request.user
            profile1 = get_object_or_404(Profile, user=user1)
            # profile1 = Profile.objects.get(user = user1)
            # profile2 = Profile.objects.get(username = username)
            profile2 = get_object_or_404(Profile, username=username)
            user2 = profile2.user
            if not profile1.first_degrees.filter(id = user2.id).exists():
                return Response({"detail": "You already don't have any connection with this profile."}, status=status.HTTP_400_BAD_REQUEST)
            profile1.first_degrees.remove(user2)
            profile2.first_degrees.remove(user1)
            
            return Response({"detail": "Connection has been removed successfully"}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"detail": "Please provide profile username"}, status=status.HTTP_400_BAD_REQUEST)


class ConnectionListView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionListSerializer

    def get_queryset(self):
        return FirstConnections.objects.filter(person = self.request.user)

