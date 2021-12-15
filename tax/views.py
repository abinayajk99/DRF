from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from restapi_app.models import *

class Schedule(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self,request,pk, format=None):
        print(pk)
        print("fetch the users tax")
        snippets = Tax.objects.using('tax').filter(user_id=pk)
        print(snippets)
        print("it to the serializer")
        serializer = TaxSerializer(snippets, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
        data=request.data
        print(data)
        serializer = TaxSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print("valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleEdit(APIView):
    def get_object(self,pk):
        try:
            return Tax.objects.using('tax').get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request,user_id, pk, format=None):
        print("----------------46-----------------------")
        snippet = self.get_object(pk)
        serializer = TaxSerializer(snippet)
        return Response(serializer.data)

    def put(self, request,user_id, pk, format=None):
        print("----------------49-----------------------")
        snippet = self.get_object(pk)
        print(snippet)
        serializer =TaxSerializer(snippet, data=request.data)
        print(serializer)
        print("----------------52-----------------------")
        if serializer.is_valid():
            print("----------------56-----------------------")
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,user_id, pk, format=None):
        '''This is for delete'''
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        