from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from RiderRegistration.models import RiderRegistrationModel
from RiderRegistration.serializers import RiderRegistrationSerializer, RiderRegistrationDetailsSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class RiderRegistration(APIView):

    def post(self,request):

        data = request.data
        serializer = RiderRegistrationSerializer(data=data)
        if serializer.is_valid():
           serializer.save()
           return Response({'message':'Rider Registered Successfully','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        
        query_type = request.query_params.get('query', None)
        value = request.query_params.get('value', None)  

        rider_data = RiderRegistrationModel.objects.all()

        if query_type == 'search' and value:
            rider_data = rider_data.filter(
                Q(rider_name__icontains=value) |
                Q(email_id__icontains=value)
            )
            if not rider_data:
                return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)
        
        elif query_type == 'sort' and value:
            rider_data = rider_data.order_by(value)
            if not rider_data:
                return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)

        paginator = PageNumberPagination()
        paginator.page_size = 10  # page size
        paginated_user_data = paginator.paginate_queryset(rider_data, request)
        
        try:
           serializer = RiderRegistrationDetailsSerializer(paginated_user_data,many=True)
           return paginator.get_paginated_response({'message': 'Rider Details','data':serializer.data})
        except:
            return Response({"message":"Something went wrong",'data':{}},status=status.HTTP_400_BAD_REQUEST)

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


