from django.core.mail import send_mail
import random
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import threading
from RiderAuthentication.models import RiderOTP

def send_email_thread(recipients, pickup_location, dropoff_location):
    
    try:
        threads = []
        for recipient in recipients:
            threads = threading.Thread(target=send_otp_email, args = [recipient,pickup_location,dropoff_location])
            threads.daemon = True
            threads.start()
        return True
    except Exception as e:
        return False

def send_otp_email(rider,pickup_location,dropoff_location):
    
    # Send OTP to the rider's email
    subject = "New Ride Request"
    message = f"""Dear {rider.rider_name},

A new ride request is available for acceptance.
Pickup location: {pickup_location}
Dropoff location: {dropoff_location}

Please login and accept the ride

Have a safe and happy ride!

If you're unable to take this ride, please ignore this email

Thank you for being a valued partner!

Best Regards,
FindMyRide

"""
    
    recipient_email = rider.email_id

    try:
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST, 
            [recipient_email])
        return Response ({"message": "OTP sent successfully.",'data': otp},status=status.HTTP_200_OK)
    except:
        return Response ({"message": "Something went wrong",'data':{}},status=status.HTTP_400_BAD_REQUEST)