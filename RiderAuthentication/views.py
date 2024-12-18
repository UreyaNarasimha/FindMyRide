from django.shortcuts import render
from RiderRegistration.models import RiderRegistrationModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
from RiderAuthentication.serializers import get_my_token
from UserLogin.utils import jwt_check


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
            is_verified = check_password(data['password'],rider.password) #verifying hased password
            if is_verified:

                data = get_my_token(rider) #generating token

                return Response({"Message":"Logged in SucssesFully",'data':data}, status=status.HTTP_201_CREATED )
        
        return Response({'Massage': 'Invalid Ridername and Password',"data":{}}, status=status.HTTP_400_BAD_REQUEST)

class RiderLogout(APIView):

    def post(self,request): 

        return Response({'message':'Rider Logged Out Successfully','data':{}},status=status.HTTP_200_OK)

class ChangePassword(APIView):

    def post(self,request):
        
        token_validation = jwt_check(request) #token validation
        if not token_validation.status_code == 200:
            return Response({'message':'Something went wrong','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        
        if 'rider_id' not in data:
            return Response({'message':'Rider ID is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'old_password' not in data:
            return Response({'message':'Old Password is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'new_password' not in data:
            return Response({'message':'New Password is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        rider = RiderRegistrationModel.objects.filter(id=data['user_id'],is_active=True).first()
        
        if rider:
            is_verified = check_password(data['old_password'],rider.password)
            if is_verified:
                password = make_password(data['new_password']) #hashing password
                rider.password = password
                rider.confirm_password = password
                rider.save()
                return Response({'message':'password updated succesfully','data':{}},
                                status=status.HTTP_200_OK)
        return Response({'message':'Something went wrong','data':{}},
                        status=status.HTTP_400_BAD_REQUEST)  