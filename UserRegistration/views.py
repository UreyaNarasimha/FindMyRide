from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from UserRegistration.models import UserRegistrationModel
from UserRegistration.serializers import UserRegistrationSerializer, UserRegistrationDetailsSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class UserRegistration(APIView):

    def post(self,request):

        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
           serializer.save()
           return Response({'message':'User Registered Successfully','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        
        query_type = request.query_params.get('query', None)
        value = request.query_params.get('value', None)  

        user_data = UserRegistrationModel.objects.all()

        if query_type == 'search' and value:
            user_data = user_data.filter(
                Q(user_name__icontains=value) |
                Q(email_id__icontains=value)
            )
            if not user_data:
                return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)
        
        elif query_type == 'sort' and value:
            user_data = user_data.order_by(value)
            if not user_data:
                return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)

        paginator = PageNumberPagination()
        paginator.page_size = 10  # page size
        paginated_user_data = paginator.paginate_queryset(user_data, request)
        
        try:
           serializer = UserRegistrationDetailsSerializer(paginated_user_data,many=True)
           return paginator.get_paginated_response({'message': 'User Details','data':serializer.data})
        except:
            return Response({"message":"Something went wrong",'data':{}},status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationDetail(APIView):

    def get_object(self,pk):
        
        return UserRegistrationModel.objects.filter(user_id=pk).first()
                
    def put(self,request,pk):
        
        user = self.get_object(pk)
        if not user:
            return Response({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = UserRegistrationDetailsSerializer(user,data=data)
        if serializer.is_valid():
           serializer.save()
           return Response({'message':'User Updated Succesfully','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'message':'Something went wrong','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk):
        
        user = self.get_object(pk) #for spefic user details
        if user:
           serializer = UserRegistrationSerializer(user)
           return Response({'message':'User Details','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self, request, pk): # for activating and deactivating users
    
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

