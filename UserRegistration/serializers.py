from rest_framework import serializers
from UserRegistration.models import UserRegistrationModel
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
import re

class UserRegistrationSerializer(serializers.ModelSerializer): 
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    confirm_password = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    student_id = serializers.CharField(required=False)
    university_name = serializers.CharField(required=False)
    
    class Meta:
        model = UserRegistrationModel
        fields = ['id','username','email','password','confirm_password','mobile_number','student_id',
                  'university_name','is_active','created_at','updated_at']
    
    
    def validate(self,validated_data):
        
        if 'username' not in validated_data:
            raise serializers.ValidationError({"message":"Username is required feild"})
        if 'email' not in validated_data:
            raise serializers.ValidationError({"message":"Email is required feild"})
        if 'password' not in validated_data:
            raise serializers.ValidationError({"message":"Password is required feild"})
        if not self.instance:
            if 'confirm_password' not in validated_data:
                raise serializers.ValidationError({"message":"Confirm Password is required feild"})
        if len(validated_data['mobile_number'])!=10:
            raise serializers.ValidationError({"message":"Mobile Number should be 10 digits"})
        if 'mobile_number' not in validated_data:
            raise serializers.ValidationError({"message":"Mobile Number is required feild"})
        if 'student_id' not in validated_data:
            raise serializers.ValidationError({"message":"StudentID is required feild"})
        if 'university_name' not in validated_data:
            raise serializers.ValidationError({"message":"University Name is required feild"})
        
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'message':"Password and Confirm Password should be same"})
        
        if not self.instance:
            if UserRegistrationModel.objects.filter(username=validated_data['username']):
                raise serializers.ValidationError({"message":"User name already exists"})
            if UserRegistrationModel.objects.filter(email=validated_data['email']):
                raise serializers.ValidationError({"message":"EmailID already exists"})
            if UserRegistrationModel.objects.filter(mobile_number=validated_data['mobile_number']):
                raise serializers.ValidationError({"message":"Mobile Number already exists"})
            if UserRegistrationModel.objects.filter(student_id=validated_data['student_id']):
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
        return UserRegistrationModel.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
         
        instance.user_name = validated_data['user_name']
        instance.email_id = validated_data['email_id']
        instance.password = make_password(validated_data['password'])
        instance.confirm_password = instance.password
        instance.mobile_number = validated_data['mobile_number']
        instance.student_id = validated_data['student_id']
        instance.university_name = validated_data['university_name']
        instance.save()
        return instance

class UserRegistrationDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRegistrationModel
        fields = ['user_id','user_name','email_id','mobile_number','student_id',
                  'university_name','is_active','created_at','updated_at']
    