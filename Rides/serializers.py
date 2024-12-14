from rest_framework import serializers
from Rides.models import AvaliableRidersModel, RideBookingModel
from UserRegistration.models import UserRegistrationModel

class AvaliableRidersserializer(serializers.ModelSerializer): 
    riders_details = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    pickup_address = serializers.CharField(required=False)
    pickup_zipcode = serializers.CharField(required=False)
    destination = serializers.CharField(required=False)
    
    class Meta:
        model = AvaliableRidersModel
        fields = ['avaliableriderslist_id','riders_details','user_id','pickup_address','pickup_zipcode',
                  'destination','is_cancelled','created_at','updated_at']
    
    def validate(self,validated_data):
        
        if 'user_id' not in validated_data:
            raise serializers.ValidationError({"message":"UserID is required feild"})
        if 'pickup_address' not in validated_data:
            raise serializers.ValidationError({"message":"Pickup Address is required feild"})
        if 'pickup_zipcode' not in validated_data:
            raise serializers.ValidationError({"message":"Pickup Zipcode is required feild"})
        if 'destination' not in validated_data:
            raise serializers.ValidationError({"message":"Destination is required feild"}) 
        if not UserRegistrationModel.objects.filter(id=validated_data['user_id'],is_active=True):
            raise serializers.ValidationError({'message':'User not found','data':{}})

        return validated_data
    
class RideBookingsSerailizer(serializers.ModelSerializer): 
    rider_id = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    pickup_address = serializers.CharField(required=False)
    pickup_zipcode = serializers.CharField(required=False)
    destination = serializers.CharField(required=False)
    
    class Meta:
        model = RideBookingModel
        fields = ['Booking_id','rider_id','user_id','pickup_address','pickup_zipcode',
                  'destination','is_cancelled','created_at','updated_at']
    
    def validate(self,validated_data):
        
        if 'user_id' not in validated_data:
            raise serializers.ValidationError({"message":"UserID is required feild"})
        if 'rider_id' not in validated_data:
            raise serializers.ValidationError({"message":"RiderID is required feild"})
        if 'pickup_address' not in validated_data:
            raise serializers.ValidationError({"message":"Pickup Address is required feild"})
        if 'pickup_zipcode' not in validated_data:
            raise serializers.ValidationError({"message":"Pickup Zipcode is required feild"})
        if 'destination' not in validated_data:
            raise serializers.ValidationError({"message":"Destination is required feild"})  
        
        return validated_data

        
        
    