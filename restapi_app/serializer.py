from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
import re
class UserSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=65, min_length=4, write_only=True,style={'input_type': 'password'})
    email = serializers.EmailField(max_length=100),
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password' ]

    def validate_username(self, username):
        if len(username) < 6 or len(username) > 15 :
            if not re.match(r'^[A-Za-z0-9]+$', username):
                raise serializers.ValidationError('Username must be include only number strings and -')
        return username

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields ="__all__"
    
    # def create(self,validated_data):
        
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company_profile=CompanyProfileSerializer(required=False,allow_null=True)
    class Meta:
        model = UserProfile
        fields = "__all__"
    def create(self, validated_data):
        data = validated_data.pop('user')
        print(data)
        print(data['username'])
        # create user 
        if  User.objects.filter(username=data['username']).exists:
            user = User.objects.db_manager('restapi_app').create(username = data['username'],first_name = data['first_name'],last_name=data['last_name'],email=data['email'],password=data['password'])
        else:
            raise serializers.ValidationError('User with the user name already exists')
        UserProfileRes = UserProfile.objects.db_manager('restapi_app').create(user = user,gender=validated_data['gender'],aboutme=validated_data['aboutme'],age=validated_data['age'],company_profile=None,is_delete=validated_data['is_delete'],)
        return UserProfileRes

    def update(self, instance,validated_data):
        data = validated_data.pop('user')
        user=User.objects.using('restapi_app').get(username=data['username'])
        user.username=data['username']
        user.first_name=data['first_name']
        user.last_name=data['last_name']
        user.email=data['email']
        user.password=data['password']
        user.save(using='restapi_app')

        instance.user=user
        instance.gender = validated_data['gender']
        instance.aboutme = validated_data['aboutme']
        instance.age = validated_data['age']
        instance.company_profile=None
        instance.is_delete =validated_data['is_delete']
        instance.save()
        return instance

   



   
   
