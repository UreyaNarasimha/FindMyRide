from django.shortcuts import render
from UserRegistration.models import UserRegistrationModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

class UserLogin(APIView):

    def post(self,request):

        data = request.data
        if 'user_name' not in data:
            return Response({'message':'Username is required feilds','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in data:
            return Response({'message':'Password is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = UserRegistrationModel.objects.filter(user_name=data['user_name'],is_active=True).first()
        
        if user:
            is_verified = check_password(data['password'],user.password)
            if is_verified:

                # refresh = RefreshToken.for_user(user)
                # access_token = str(refresh.access_token)
                # refresh_token = str(refresh)

                # token = {
                #     'access_token': access_token,
                #     'refresh_token': refresh_token
                # }
                
                return Response({"Message":"Logged in SucssesFully",'data':{}}, status=status.HTTP_201_CREATED )
        
        return Response({'Massage': 'Invalid Username and Password',"data":{}}, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):

    def post(self,request): 

        return Response({'message':'User Logged Out Successfully','data':{}},status=status.HTTP_200_OK)
        