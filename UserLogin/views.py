from django.shortcuts import render
from UserRegistration.models import UserRegistrationModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
# from rest_framework_simplejwt.tokens import RefreshToken
import random
import string

class UserLogin(APIView):

    def post(self,request):
        
        data = request.data
        if 'user_name' not in data:
            return Response({'message':'Username is required feilds','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in data:
            return Response({'message':'Password is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if 'captcha' not in data:
            return Response({'message':'Captcha is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Get stored CAPTCHA from session
        stored_captcha = request.session.get('captcha_text')

        # Verify the CAPTCHA
        if not data['captcha'] == stored_captcha:
           return Response({"message": "CAPTCHA verification failed.",'data':{}}, status=status.HTTP_400_BAD_REQUEST)
        
        user = UserRegistrationModel.objects.filter(user_name=data['user_name'],is_active=True).first()
        
        if user:
            is_verified = check_password(data['password'],user.password)
            if is_verified:
                
                # refresh = RefreshToken.for_user(user)
                # access_token = str(refresh.access_token)

                # token  = {
                #     "refresh_token": refresh,
                #     "access_token": access_token
                # }
                
                return Response({"Message":"Logged in SucssesFully",'data':{}}, status=status.HTTP_201_CREATED )
        
        return Response({'Massage': 'Invalid Username and Password',"data":{}}, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):

    def post(self,request): 

        return Response({'message':'User Logged Out Successfully','data':{}},status=status.HTTP_200_OK)
    
class Captcha(APIView):

    def get(self, request):
        # Generate CAPTCHA text
        captcha_text = Captcha.CaptchaGeneartor()

        # Store CAPTCHA text in session
        request.session['captcha_text'] = captcha_text

        return Response({"message":"Captcha","data": captcha_text}, status=status.HTTP_200_OK)
    
    def CaptchaGeneartor():
            # Generate a random string (6 alphanumeric characters)
            captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            return captcha_text
