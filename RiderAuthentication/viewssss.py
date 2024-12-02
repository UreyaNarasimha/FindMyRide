from django.shortcuts import render
from RiderRegistration.models import RiderRegistrationModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password


class RiderLogin(APIView):

    def post(self,request):

        data = request.data
        if 'rider_name' not in data:
            return Response({'message':'Rider name is required feilds','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in data:
            return Response({'message':'Password is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        rider = RiderRegistrationModel.objects.filter(rider_name=data['rider_name'],is_active=True).first()
        
        if rider:
            is_verified = check_password(data['password'],rider.password)
            if is_verified:
                return Response({"Message":"Logged in SucssesFully",'data':{}}, status=status.HTTP_201_CREATED )
        
        return Response({'Massage': 'Invalid Ridername and Password',"data":{}}, status=status.HTTP_400_BAD_REQUEST)

class RiderLogout(APIView):

    def post(self,request): 

        return Response({'message':'Rider Logged Out Successfully','data':{}},status=status.HTTP_200_OK)
        