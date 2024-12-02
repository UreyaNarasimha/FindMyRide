from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from RiderRegistration.models import RiderRegistrationModel
from RiderRegistration.serializers import RiderRegistrationSerializer

class RiderRegistration(APIView):

    def post(self,request):

        data = request.data
        serializer = RiderRegistrationSerializer(data=data)
        if serializer.is_valid():
           serializer.save()
           return Response({'message':'Rider Registered Successfully','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        
        rider_data = RiderRegistrationModel.objects.all()
        serializer = RiderRegistrationSerializer(rider_data,many=True)
        return Response({'message':serializer.data},status=status.HTTP_200_OK)

class RiderRegistrationDetail(APIView):

    def get_object(self,pk):
        
        return RiderRegistrationModel.objects.filter(rider_id=pk).first()
                
    def put(self,request,pk):
        
        rider = self.get_object(pk)
        if not rider:
            return Response({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = RiderRegistrationSerializer(rider,data=data)
        if serializer.is_valid():
           serializer.save()
           return Response({'message':'Rider Updated Succesfully','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'message':'Something went wrong','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk):
        
        rider = self.get_object(pk)
        if rider:
           serializer = RiderRegistrationSerializer(rider)
           return Response({'message':'Rider Details','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self, request, pk):
    
        rider = self.get_object(pk)
        if not rider:
            return Response({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
        if rider.is_active:
            rider.is_active = False
            message = 'Rider Deleted Successfully'
        else:
            rider.is_active=True
            message = 'Rider Activated Successfully'
        rider.save()
        serializer = RiderRegistrationSerializer(rider)
        return Response({'message': message,'data':serializer.data},status=status.HTTP_200_OK)


