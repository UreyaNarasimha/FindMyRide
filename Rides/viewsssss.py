from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Rides.models import RideBookings
from Rides.serializers import Ridesserializer
from UserRegistration.models import UserRegistrationModel
from RiderRegistration.models import RiderRegistrationModel

class RiderBookings(APIView):

    def post(self,request):

        data = request.data
     
        serializer = Ridesserializer(data=data)
        if serializer.is_valid():
           serializer.save()
           
           user_details = UserRegistrationModel.objects.filter(user_id=data['user_id'],is_active=True)
           if not user_details:
              return Response({'message':'User not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
           rider_details = RiderRegistrationModel.objects.filter(rider_id=data['rider_id'],is_active=True)
           if not rider_details:
              return Response({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
           
           avaliable_riders = RiderRegistrationModel.objects.filter(zipcode=data['pickup_zipcode'])
           if avaliable_riders:
                rider_details = []
                for avaliable_rider in avaliable_riders:
                    booking = {
                        'rider_name':avaliable_rider.rider_name,
                        'rider_mobile_number':avaliable_rider.mobile_number
                    } 
                    rider_details.append(booking)

                return Response({'message':'Booking Successfull','data':serializer.data},status=status.HTTP_201_CREATED)
           return Response({'message':'Riders not avliable at this location','data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    # def get(self,request):
        
    #     rider_data = RiderRegistrationModel.objects.all()
    #     serializer = RiderRegistrationSerializer(rider_data,many=True)
    #     return Response({'message':serializer.data},status=status.HTTP_200_OK)

# class RiderRegistrationDetail(APIView):

#     def get_object(self,pk):
        
#         return RiderRegistrationModel.objects.filter(rider_id=pk).first()
                
#     def put(self,request,pk):
        
#         rider = self.get_object(pk)
#         if not rider:
#             return Response({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
        
#         data = request.data
#         serializer = RiderRegistrationSerializer(rider,data=data)
#         if serializer.is_valid():
#            serializer.save()
#            return Response({'message':'Rider Updated Succesfully','data':serializer.data},status=status.HTTP_201_CREATED)
#         return Response({'message':'Something went wrong','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
#     def get(self,request,pk):
        
#         rider = self.get_object(pk)
#         if rider:
#            serializer = RiderRegistrationSerializer(rider)
#            return Response({'message':'Rider Details','data':serializer.data},status=status.HTTP_200_OK)
#         return Response({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)

        
#     def delete(self, request, pk):
    
#         rider = self.get_object(pk)
#         if not rider:
#             return Response({'message':'Rider not found','data':{}},status=status.HTTP_400_BAD_REQUEST)
#         if rider.is_active:
#             rider.is_active = False
#             message = 'Rider Deleted Successfully'
#         else:
#             rider.is_active=True
#             message = 'Rider Activated Successfully'
#         rider.save()
#         serializer = RiderRegistrationSerializer(rider)
#         return Response({'message': message,'data':serializer.data},status=status.HTTP_200_OK)


