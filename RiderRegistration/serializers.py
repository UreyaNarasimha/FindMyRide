from rest_framework import serializers
from RiderRegistration.models import RiderRegistrationModel
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
import re

class RiderRegistrationSerializer(serializers.ModelSerializer): 
    rider_name = serializers.CharField(required=False)
    email_id = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    confirm_password = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    student_id = serializers.CharField(required=False)
    university_name = serializers.CharField(required=False)
    drivers_license_id = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    zipcode = serializers.CharField(required=False)
    
    class Meta:
        model = RiderRegistrationModel
        fields = ['id','rider_name','email_id','password','confirm_password','mobile_number','student_id',
                  'university_name','drivers_license_id','address','zipcode','is_active','created_at','updated_at']
    
    def validate(self,validated_data):
        
        if 'rider_name' not in validated_data:
            raise serializers.ValidationError({"message":"Rider name is required feild"})
        if 'email_id' not in validated_data:
            raise serializers.ValidationError({"message":"EmailID is required feild"})
        if 'password' not in validated_data:
            raise serializers.ValidationError({"message":"Password is required feild"})
        if not self.instance:
            if 'confirm_password' not in validated_data:
                raise serializers.ValidationError({"message":"Confirm Password is required feild"})
        if 'mobile_number' not in validated_data:
            raise serializers.ValidationError({"message":"Mobile Number is required feild"})
        if len(validated_data['mobile_number'])!=10:
            raise serializers.ValidationError({"message":"Mobile Number should be 10 digits"})
        if 'student_id' not in validated_data:
            raise serializers.ValidationError({"message":"StudentID is required feild"})
        if 'university_name' not in validated_data:
            raise serializers.ValidationError({"message":"University Name is required feild"})
        if 'address' not in validated_data:
            raise serializers.ValidationError({"message":"Address is required feild"})
        if 'zipcode' not in validated_data:
            raise serializers.ValidationError({"message":"Zipcode is required feild"})

        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'message':"Password and Confirm Password should be same"})
        
        if not self.instance:
            if RiderRegistrationModel.objects.filter(rider_name=validated_data['rider_name']):
                raise serializers.ValidationError({"message":"Rider name already exists"})
            if RiderRegistrationModel.objects.filter(email_id=validated_data['email_id']):
                raise serializers.ValidationError({"message":"EmailID already exists"})
            if RiderRegistrationModel.objects.filter(mobile_number=validated_data['mobile_number']):
                raise serializers.ValidationError({"message":"Mobile Number already exists"})
            if RiderRegistrationModel.objects.filter(student_id=validated_data['student_id']):
                raise serializers.ValidationError({"message":"StudentID already exists"})
        
        return validated_data
    
    def validate_email_id(self,email_id):
        
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]{5,}+\.[a-zA-Z]{3,}$'
        if not re.match(regex, email_id):
            raise serializers.ValidationError({"message":"Invalid Email Format"})
        return email_id
        
    def create(self, validated_data):
            
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['confirm_password'] = make_password(validated_data.get('confirm_password'))
        return RiderRegistrationModel.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
         
        instance.rider_name = validated_data['rider_name']
        instance.email_id = validated_data['email_id']
        instance.password = make_password(validated_data['password'])
        instance.confirm_password = instance.password
        instance.mobile_number = validated_data['mobile_number']
        instance.student_id = validated_data['student_id']
        instance.university_name = validated_data['university_name']
        instance.address = validated_data['address']
        instance.zipcode = validated_data['zipcode']
        instance.save()
        return instance

class RiderRegistrationDetailsSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = RiderRegistrationModel
        fields = ['rider_id','rider_name','email_id','mobile_number','student_id','university_name',
                  'drivers_license_id','address','zipcode','is_active','created_at','updated_at']