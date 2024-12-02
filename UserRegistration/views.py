from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from UserRegistration.models import UserRegistrationModel
from UserRegistration.serializers import UserRegistrationSerializer

class UserRegistration(APIView):

    def post(self,request):

        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
           serializer.save()
           return Response({'message':'User Registered Successfully','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        
        user_data = UserRegistrationModel.objects.all()
        serializer = UserRegistrationSerializer(user_data,many=True)
        return Response({'message':serializer.data},status=status.HTTP_200_OK)

class UserRegistrationDetail(APIView):

    def get_object(self,pk):
        
        return UserRegistrationModel.objects.filter(user_id=pk).first()
                
    def put(self,request,pk):
        
        user = self.get_object(pk)
        if not user:
            return Response({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = UserRegistrationSerializer(user,data=data)
        if serializer.is_valid():
           serializer.save()
           return Response({'message':'User Updated Succesfully','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'message':'Something went wrong','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk):
        
        user = self.get_object(pk)
        if user:
           serializer = UserRegistrationSerializer(user)
           return Response({'message':'User Details','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self, request, pk):
    
        user = self.get_object(pk)
        if not user:
            return Response({'message':'User not found'},status=status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            user.is_active = False
            message = 'User Deleted Successfully'
        else:
            user.is_active=True
            message = 'User Activated Successfully'
        user.save()
        serializer = UserRegistrationSerializer(user)
        return Response({'message': message,'data':serializer.data},status=status.HTTP_200_OK)


