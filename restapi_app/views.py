from django.shortcuts import render
from django.contrib.auth.models import User
from restapi_app.serializer import UserSerializer,UserProfileSerializer,CompanyProfileSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *

# Create your views here.
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()

from rest_framework import generics, permissions, serializers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import datetime

from oauth2_provider.models import AccessToken,Application,RefreshToken
from rest_framework.authtoken.models import Token 
import requests,json
from django.contrib.auth import logout

class Signup(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetSoftDestroyDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def destroy(self, request, pk=None, **kwargs):
        request.user.is_active = False
        request.user.save()
        return Response("user set to inactive")

class SnippetDestroyDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def destroy(self, request, pk=None, **kwargs):
        request.user.delete()
        return Response("user is deleted")

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        data=request.data
        username = data.get('username')
        password = data.get('password')
        user =  authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                token=''
                time_threshold=datetime.now()
                token_obj = AccessToken.objects.filter(user=user,expires__gt=time_threshold)
                if token_obj:
                    token_obj = token_obj[0]
                    token = token_obj.token
                else:
                    if not Application.objects.filter(user=1).exists:
                        Application.objects.create(user_id=1,authorization_grant_type = 'password',client_type='confidential')
                    app_obj = Application.objects.filter(user=1)
                    if  app_obj:
                        app_obj = app_obj[0]
                        client_id = app_obj.client_id
                        client_secret = app_obj.client_secret
                        url='http://'+request.get_host()+'/o/token/'
                        data_dict = {'grant_type':'password','username':username,'password':password,'client_id':client_id,'client_secret':client_secret}
                        aa = requests.post(url,data=data_dict)
                        data = json.loads(aa.text)
                        token =data.get('access_token','')
                request.session['token']=token
                return HttpResponse(token)
            else:
                return HttpResponse("Account was inactive")
        else:
            return HttpResponse("user name or password id incorrect | user is in_active")
    else:
        return HttpResponse("Something is wrong")


class TokenRefresh(APIView):
    def post(self,request,format=None):
        data=request.data
        user_id=data['user_id']
        client_id=data['client_id']
        client_secret=data['client_secret']
        token_obj = RefreshToken.objects.filter(user=user_id).order_by("-id")
        refresh_token=''
        if token_obj:
            token_obj=token_obj[0]
            refresh_token=token_obj.token
        url='http://'+request.get_host()+'/o/token/'
        data_dict = {'grant_type':'refresh_token','client_id':client_id,'client_secret':client_secret,'refresh_token':refresh_token}
        aa=requests.post(url,data=data_dict)
        data=json.loads(aa.text)
        return Response(data,status=status.HTTP_201_CREATED)


def logout_view(request):
    logout(request)
    return HttpResponse("logout")



class UserList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            obj=UserProfile.objects.get(pk=pk)
            return obj
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = UserProfile.objects.get(pk=pk)
        serializer = UserProfileSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet =UserProfile.objects.get(pk=pk)
        serializer = UserProfileSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CompanyList(APIView):
    def get(self, request,pk, format=None):
        users = UserProfile.objects.get(id=pk)
        data=users.company_profile
        
        if data == None:
            return Response("None")
        else:
            serializer = CompanyProfileSerializer(data)
            return Response(serializer.data)

    def post(self,request,pk,format=None):
        data=request.data
        datavalue=CompanyProfile.objects.create(company_name=data['company_name'],company_grade=data['company_grade'],address=data['address'],designation=data['designation'],salary=data['salary'])
        user_data = UserProfile.objects.get(id=pk)
        user_data.company_profile=datavalue
        user_data.save()
        serializer = CompanyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetail(APIView):
    
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, request,pk,company_id,):
        try:
            obj=CompanyProfile.objects.get(pk=company_id)
            return obj
        except obj.DoesNotExist:
            raise Http404

    def get(self, request, pk,company_id, format=None):
        company = CompanyProfile.objects.get(pk=company_id)
        serializer=CompanyProfileSerializer(company)
        return Response(serializer.data)

    def put(self, request, pk,company_id, format=None):
        snippet =CompanyProfile.objects.get(pk=company_id)
        data=request.data
        snippet.company_name=data['company_name']
        snippet.company_grade=data['company_grade']
        snippet.address=data['address']
        snippet.designation=data['designation']
        snippet.salary=data['salary']
        snippet.save()
        serializer = CompanyProfileSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk,company_id, format=None):
        snippet =CompanyProfile.objects.get(pk=company_id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



