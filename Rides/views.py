from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Rides.serializers import AvaliableRidersserializer, RideBookingsSerailizer
from Rides.models import AvaliableRidersModel, RideBookingModel, BookingLogs, AvaliableRidersLogs
from RiderRegistration.models import RiderRegistrationModel
from UserRegistration.models import UserRegistrationModel
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
import csv
import os
import json
from datetime import datetime

class AvaliableRiders(APIView):

    def post(self,request):

        data = request.data
        
        serializer = AvaliableRidersserializer(data=data)
        if serializer.is_valid():
           serializer.save()
           
           avaliable_riders = RiderRegistrationModel.objects.filter(zipcode=data['pickup_zipcode'])
           if avaliable_riders:
                riders_details = []
                for avaliable_rider in avaliable_riders:
                    if RideBookingModel.objects.filter(rider_id = avaliable_rider.rider_id,
                                                       is_ride_completed = False).exists():
                        pass
                    else:
                        booking = {
                            'rider_id':avaliable_rider.rider_id,
                            'rider_name':avaliable_rider.rider_name,
                            'rider_mobile_number':avaliable_rider.mobile_number
                        } 
                        riders_details.append(booking)
                
                if not riders_details:
                    return Response({'message':'Riders not avliable at this location','data':{}},
                                status=status.HTTP_400_BAD_REQUEST)

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
            
            query_type = request.query_params.get('query', None)
            value = request.query_params.get('value', None)  

            avaliable_riders_data = AvaliableRidersModel.objects.all()

            if query_type == 'search' and value:
                avaliable_riders_data = avaliable_riders_data.filter(
                    Q(avaliableriderslist_id__icontains=value) |
                    Q(rider_id__icontains=value) |
                    Q(user_id__icontains=value) |
                    Q(pickup_address__icontains=value) |
                    Q(pickup_zipcode__icontains=value) |
                    Q(destination__icontains=value) |
                    Q(is_cancelled__icontains=value)
                )
                if not avaliable_riders_data:
                    return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)
            
            elif query_type == 'sort' and value:
                avaliable_riders_data = avaliable_riders_data.order_by(value)
                if not avaliable_riders_data:
                    return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)

            paginator = PageNumberPagination()
            paginator.page_size = 10  # page size
            paginated_user_data = paginator.paginate_queryset(avaliable_riders_data, request)
            
            try:
              serializer = AvaliableRidersserializer(paginated_user_data,many=True)
              return paginator.get_paginated_response({'message': 'Avaliable Riders data Details','data':serializer.data})
            except:
                return Response({"message":"Something went wrong",'data':{}},status=status.HTTP_400_BAD_REQUEST)

class RideBookings(APIView):

    def post(self,request):

        data = request.data
        
        if 'avaliableriderslist_id' not in data:            
            return Response({"message":"AvaliableRidersList Id is required feild",'data':{}}, 
                             status=status.HTTP_400_BAD_REQUEST) 

        serializer = RideBookingsSerailizer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            avaliable_riders_obj = AvaliableRidersModel.objects.filter(avaliableriderslist_id=data['avaliableriderslist_id'])
            if not avaliable_riders_obj:
                return Response({"message":"Something went wrong or Ride is cancelled",'data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
            if not avaliable_riders_obj.filter(user_id = data['user_id']):
                return Response({"message":"User Id is mismatching",'data':{}},
                                status=status.HTTP_400_BAD_REQUEST)
            if not avaliable_riders_obj.filter(riders_details__contains=[{'rider_id': int(data['rider_id'])}]):
                return Response({"message":"Rider Id is mismatching",'data':{}},
                                status=status.HTTP_400_BAD_REQUEST)

            user_details = UserRegistrationModel.objects.filter(user_id=data['user_id'],is_active=True).first()
            if not user_details:
               return Response ({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
            rider_details = RiderRegistrationModel.objects.filter(rider_id=data['rider_id'],is_active=True).first()
            if not rider_details:
               return Response ({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
            
            del data['avaliableriderslist_id']

            try:
                booking_obj = RideBookingModel.objects.create(**data)
                booking_obj.is_ride_completed = False
                booking_obj.save()
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

    def get(self,request):
            
            query_type = request.query_params.get('query', None)
            value = request.query_params.get('value', None)  

            rides_data = RideBookingModel.objects.all()

            if query_type == 'search' and value:
                rides_data = rides_data.filter(
                    Q(Booking_id__icontains=value) |
                    Q(rider_id__icontains=value) |
                    Q(user_id__icontains=value) |
                    Q(pickup_address__icontains=value) |
                    Q(pickup_zipcode__icontains=value) |
                    Q(destination__icontains=value) |
                    Q(is_cancelled__icontains=value)
                )
                if not rides_data:
                    return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)
            
            elif query_type == 'sort' and value:
                rides_data = rides_data.order_by(value)
                if not rides_data:
                    return Response({"message":"No Data Found",'data':{}},status=status.HTTP_400_BAD_REQUEST)

            paginator = PageNumberPagination()
            paginator.page_size = 2  # page size
            paginated_user_data = paginator.paginate_queryset(rides_data, request)
            
            try:
              serializer = RideBookingsSerailizer(paginated_user_data,many=True)
              return paginator.get_paginated_response({'message': 'Rides Details','data':serializer.data})
            except:
                return Response({"message":"Something went wrong",'data':{}},status=status.HTTP_400_BAD_REQUEST)
            
class UpdateRiderStatus(APIView):

    def put(self, request, pk):
        
        ride_obj = RideBookingModel.objects.filter(Booking_id=pk).first()
        if not ride_obj:
            return Response({'message':'No data found','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if ride_obj.is_ride_completed:
            return Response({'message':'Ride already completed','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        ride_obj.is_ride_completed = True
        ride_obj.save()
        return Response({'message':'Ride completed successfully','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)

class CSVFileGenerator(APIView):

    def RideBookingsCsv(self,request):
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = 'ridesbookings_{}_csv'.format(timestamp)
        file_path = os.path.join(r'', file_name)  # Replace with your desired directory

        data = RideBookingModel.objects.all()

        header_mapping = {
            "Booking_id": "Booking ID",
            "user_id" : "User ID",
            "rider_id" : "Rider ID",
            "pickup_address" : "Pickup Address",
            "pickup_zipcode" : "Pickup Zipcode",
            "destination" : "Destination",
            "is_cancelled" : "Is Cancelled",
            "is_ride_completed" : "Is Ride Completed",
            "created_at" : "Created At",
            "updated_at": "Updated At"
        }
        
        with open(file_path,'w+', encoding='utf-8') as data_file:
            writer = csv.DictWriter(data_file, fieldnames = header_mapping,
                                    quoting = csv.QUOTE_ALL)
            writer.writerow(header_mapping)
        
            for i in data:
                rides_booking_dict = i.__dict__

                del rides_booking_dict['_state']

                try:
                    writer.writerow(rides_booking_dict)
                except:
                    writer.writerow({k:json.dumps(str(v)) for k,v in rides_booking_dict.items()})
                    continue
        
        data_file.close()
                
        return Response({'message':'file {} downloaded successfully'.format(file_name),'data':{}},
                        status=status.HTTP_200_OK)


    def AvaliableRidersCsv(self,request):
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = 'avaliableriders_{}_csv'.format(timestamp)
        file_path = os.path.join(r'', file_name)  # Replace with your desired directory

        data = AvaliableRidersModel.objects.all()

        header_mapping = {
            "avaliableriderslist_id": "AvaliableRiderslist ID",
            "user_id" : "User ID",
            "riders_details" : "Riders Details",
            "pickup_address" : "Pickup Address",
            "pickup_zipcode" : "Pickup Zipcode",
            "destination" : "Destination",
            "is_cancelled" : "Is Cancelled",
            "created_at" : "Created At",
            "updated_at": "Updated At"
        }
        
        with open(file_path,'w+', encoding='utf-8') as data_file:
            writer = csv.DictWriter(data_file, fieldnames = header_mapping,
                                    quoting = csv.QUOTE_ALL)
            writer.writerow(header_mapping)

            for i in data:
                avaliable_riders_dict = i.__dict__

                del avaliable_riders_dict['_state']

                try:
                    writer.writerow(avaliable_riders_dict)
                except:
                    writer.writerow({k:json.dumps(str(v)) for k,v in avaliable_riders_dict.items()})
                    continue
        
        data_file.close()
                
        return Response({'message':'file {} downloaded successfully'.format(file_name),'data':{}},
                        status=status.HTTP_200_OK)
    
    def post(self,request):

        action = request.query_params.get('action')  
        if not action:
            return Response({"message": "Action is required feild",'data':{}}, 
                            status=status.HTTP_400_BAD_REQUEST)
        if action == 'RideBookingsCsv':
            return self.RideBookingsCsv(request)
        elif action == 'AvaliableRidersCsv':
            return self.AvaliableRidersCsv(request)
        return Response({"message": "Invalid action",'data':{}}, status=status.HTTP_400_BAD_REQUEST)