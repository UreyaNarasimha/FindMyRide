from rest_framework import serializers
from Rides.models import RideBookings
from rest_framework.response import Response
from rest_framework import status
import re

class Ridesserializer(serializers.ModelSerializer): 
    rider_id = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    pickup_address = serializers.CharField(required=False)
    pickup_zipcode = serializers.CharField(required=False)
    destination = serializers.CharField(required=False)
    
    class Meta:
        model = RideBookings
        fields = ['booking_id','rider_id','user_id','pickup_address','pickup_zipcode',
                  'destination','is_cancelled','created_at','updated_at']
    
    def validate(self,validated_data):
        
        if 'rider_id' not in validated_data:
            raise serializers.ValidationError({"message":"RiderID is required feild"})
        if 'user_id' not in validated_data:
            raise serializers.ValidationError({"message":"UserID is required feild"})
        if 'pickup_address' not in validated_data:
            raise serializers.ValidationError({"message":"Pickup Address is required feild"})
        if 'pickup_zipcode' not in validated_data:
            raise serializers.ValidationError({"message":"Pickup Zipcode is required feild"})
        if 'destination' not in validated_data:
            raise serializers.ValidationError({"message":"Destination is required feild"})
        
        return validated_data
        
    def create(self, validated_data):
            
        return RideBookings.objects.create(**validated_data)
        
    