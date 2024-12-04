from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Rides.serializers import AvaliableRidesserializer, RideBookingsSerailizer
from Rides.models import AvaliableRidersModel, RideBookingModel, BookingLogs, AvaliableRidersLogs
from RiderRegistration.models import RiderRegistrationModel
from UserRegistration.models import UserRegistrationModel

class AvaliableRiders(APIView):

    def post(self,request):

        data = request.data
        
        serializer = AvaliableRidesserializer(data=data)
        if serializer.is_valid():
           serializer.save()

           avaliable_riders = RiderRegistrationModel.objects.filter(zipcode=data['pickup_zipcode'])
           if avaliable_riders:
                riders_details = []
                for avaliable_rider in avaliable_riders:
                    booking = {
                        'rider_id':avaliable_rider.rider_id,
                        'rider_name':avaliable_rider.rider_name,
                        'rider_mobile_number':avaliable_rider.mobile_number
                    } 
                    riders_details.append(booking)
                
                avaliable_riders_details = {
                    'user_id': data['user_id'],
                    'pickup_address':data['pickup_address'],
                    'pickup_zipcode':data['pickup_zipcode'],
                    'destination':data['destination'],
                    'riders_details': riders_details
                }
                
                try:
                    avaliableriders_obj = AvaliableRidersModel.objects.create(**avaliable_riders_details)
                except:
                    return Response({'message':'Something went wrong','data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
                
           else:
                return Response({'message':'Riders not avliable at this location','data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
           
           avaliable_riders_details['avaliableriderslist_id'] = avaliableriders_obj.avaliableriderslist_id

           log = {
               'avaliableriders_details': avaliable_riders_details
           }

           try:
               AvaliableRidersLogs.objects.create(**log)
           except:
               return Response({'message':'Something went wrong','data':{}},status=status.HTTP_400_BAD_REQUEST)
           
           return Response({'message':'Avaliable Riders','data':avaliable_riders_details},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):

        rider_data = AvaliableRidersModel.objects.all()
        serializer = AvaliableRidersModel(rider_data,many=True)
        return Response({'message':serializer.data},status=status.HTTP_200_OK)
    
class RideBookings(APIView):

    def post(self,request):

        data = request.data
        
        if not data['avaliableriderslist_id']:            
            return Response({"message":"AvaliableRidersList Id is required feild"}, 
                             status=status.HTTP_400_BAD_REQUEST) 
        
        if not AvaliableRidersModel.objects.filter(avaliableriderslist_id=data['avaliableriderslist_id'],
                                                   is_cancelled=False):
            return Response({"message":"Something went wrong or Ride is cancelled"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = RideBookingsSerailizer(data=data)
        if serializer.is_valid():
            serializer.save()

            user_details = UserRegistrationModel.objects.filter(user_id=data['user_id'],is_active=True).first()
            if not user_details:
               return Response ({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
            rider_details = RiderRegistrationModel.objects.filter(rider_id=data['rider_id'],is_active=True).first()
            if not rider_details:
               return Response ({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
            
            del data['avaliableriderslist_id']

            try:
                booking_obj = RideBookingModel.objects.create(**data)
            except:
                return Response({'message':'Something went wrong','data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
            
            booking_details = { 'booking_id': booking_obj.Booking_id,
                                'user_details': {
                                    'user_id': user_details.user_id,
                                    'user_name': user_details.user_name,
                                    'user_mobile_number':user_details.mobile_number
                                },
                                'rider_details': {
                                    'rider_id': rider_details.rider_id,
                                    'rider_name': rider_details.rider_name,
                                    'rider_mobile_number':rider_details.mobile_number
                                },
                                'pickup_address': booking_obj.pickup_address,
                                'pickup_zipcode': booking_obj.pickup_address,
                                'destination': booking_obj.destination
            }
            
            #creating logs
            log = {
                'booking_id' : booking_obj.Booking_id,
                'booking_details': booking_details
            }
            try:
               BookingLogs.objects.create(**log)
            except:
                return Response({'message':'Something went wrong','data':{}},status=status.HTTP_400_BAD_REQUEST)

            return Response({'message':'Booking Successfull','data':booking_details},status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors,'data':{}},status=status.HTTP_400_BAD_REQUEST)
