from django.shortcuts import render
from UserRegistration.models import UserRegistrationModel
from UserLogin.models import OTP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
from datetime import datetime, timedelta
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from UserLogin.serializers import get_my_token
from django.contrib.auth.hashers import check_password, make_password
from UserLogin.utils import jwt_check

class UserLogin(APIView):
    
    def post(self,request):
        
        data = request.data
        if 'username' not in data:
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
        generated_time = request.session.get('captcha_generated_time')
        
        # Verify the CAPTCHA
        if not data['captcha'] == stored_captcha:
           return Response({"message": "CAPTCHA verification failed.",'data':{}}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        generated_time = datetime.fromisoformat(generated_time)
        expiry_time = timedelta(minutes=5)  # expiry duration (5 minutes)
        if datetime.now() - generated_time > expiry_time:
            return Response({"message": "CAPTCHA Expired",'data':{}}, 
                            status=status.HTTP_400_BAD_REQUEST)

        user = UserRegistrationModel.objects.filter(username=data['username'],is_active=True).first()
        
        if user:
            is_verified = check_password(data['password'],user.password)
            if is_verified:

                data = get_my_token(user)
                            
                #sending OTP               
                try:
                    otp = SendOTP(user)  
                except:
                    return Response({"Message":"Something went wrong",'data': {}}, 
                                    status=status.HTTP_400_BAD_REQUEST)

                return Response({"Message":"Logged in SucssesFully",'data': data}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Invalid Username and Password',"data":{}}, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):

    def post(self,request): 

        return Response({'message':'User Logged Out Successfully','data':{}},status=status.HTTP_200_OK)
    
class Captcha(APIView):

    def get(self, request):
        # Generate CAPTCHA text
        captcha_text = Captcha.CaptchaGeneartor()

        # Store CAPTCHA text in session
        request.session['captcha_text'] = captcha_text
        request.session['captcha_generated_time'] = datetime.now().isoformat()

        return Response({"message":"Captcha","data": captcha_text}, status=status.HTTP_200_OK)
    
    def CaptchaGeneartor():
            # Generate a random string (6 alphanumeric characters)
            captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            return captcha_text

class OTPGenerator(APIView):

    def post(self,request):

        data = request.data
        
        if 'user_id' not in data:
            return Response({'message':'User ID is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)

        user_obj = UserRegistrationModel.objects.filter(user_id = data['user_id'],is_active = True).first()
        if not user_obj:
            return Response({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            otp = SendOTP(user_obj) #sending OTP
            return otp
        except:
            return Response ({"message": "Something went wrong",'data':{}},
                             status=status.HTTP_400_BAD_REQUEST)

class OTPVerification(APIView):

    def post(self,request):
        
        try:
            data = request.data

            if 'user_id' not in data:
                return Response({'message':'User ID is required feild','data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
            if 'otp' not in data:
                return Response({'message':'otp is required feild','data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
            
            user_obj = UserRegistrationModel.objects.filter(user_id=data['user_id'],is_active=True).first()
            if not user_obj:
                return Response({'message':'User not found','data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
            
            #validating whether the otp belongs to correct user or not
            otp_obj = OTP.objects.filter(user_id=data['user_id'],otp=data['otp']).first() 
            if not otp_obj:
                return Response({'message':'Invalid OTP!','data':{}},status=status.HTTP_400_BAD_REQUEST)            
            
            #validating expiry
            expiry_time = otp_obj.created_at+timedelta(minutes=5)
            if otp_obj.is_expired == True or now() > expiry_time:
                return Response({'message':'OTP Expired','data':{}},status=status.HTTP_400_BAD_REQUEST)
            
            otp_obj.is_expired = True #making otp as expired after validating
            otp_obj.save()
            return Response({'message':'OTP Verified Successfully','data':{}},status=status.HTTP_200_OK)            
        
        except:
            return Response({'message':'Something went wrong','data':{}},status=status.HTTP_400_BAD_REQUEST)  

class ChangePassword(APIView):

    def post(self,request):
        
        token_validation = jwt_check(request) #token validation
        if not token_validation.status_code == 200:
            return Response({'message':'Something went wrong','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        
        if 'user_id' not in data:
            return Response({'message':'User ID is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'old_password' not in data:
            return Response({'message':'Old Password is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'new_password' not in data:
            return Response({'message':'New Password is required feild','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = UserRegistrationModel.objects.filter(id=data['user_id'],is_active=True).first()
        
        if user:
            is_verified = check_password(data['old_password'],user.password)
            if is_verified:
                password = make_password(data['new_password']) #hashing password
                user.password = password
                user.confirm_password = password
                user.save()
                return Response({'message':'password updated succesfully','data':{}},
                                status=status.HTTP_200_OK)
        return Response({'message':'Something went wrong','data':{}},
                        status=status.HTTP_400_BAD_REQUEST)          

def SendOTP(user):

    """
    Generate and send an OTP to the user's email.
    """
    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)
    
    otp_data = {
        'user_id' : user.id,
        'otp' : otp
    }
    
    #making previously requested otps expired when user requests new otps
    unexpired_otps = OTP.objects.filter(user_id = user.id, is_expired = False)
    for unexpired_otp in unexpired_otps:
        unexpired_otp.is_expired = True
    OTP.objects.bulk_update(unexpired_otps, fields=['is_expired'])

    try:
        OTP.objects.create(**otp_data)
    except:
        return Response ({"message": "Something went wrong",'data':{}},status=status.HTTP_400_BAD_REQUEST)
   
    # Send OTP to the user's email
    subject = "Your OTP Code"
    message = f""" Dear {user.username},
    
Your OTP code is {otp}. 
This code is valid for 5 minutes.
    
If you didn't request this otp, please ignore this email

Thank you for being a valued partner!

Best Regards,
FindMyRide
    
    """
    recipient_email = user.email

    try:
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST, 
            [recipient_email])
        return Response ({"message": "OTP sent successfully.",'data': otp},status=status.HTTP_200_OK)
    except:
        return Response ({"message": "Something went wrong",'data':{}},status=status.HTTP_400_BAD_REQUEST)