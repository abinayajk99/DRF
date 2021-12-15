
from django.contrib.auth.models import User
from rest_framework import serializers
# from djongo import models
from .models import *

from abc import ABCMeta, abstractmethod
from rest_framework import serializers



# class IncomeSerializer(serializers.Serializer):
#     __metaclass__ = ABCMeta
#     class Meta:
#         model = Income
#         fields ="__all__"
#         abstract=True
        
#     @abstractmethod
#     def validate(self, data):
#         # Doing validation stuff with "course" and "students" fields
#         ...
#         return data

# class ExpenseSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Expense
#         fields ="__all__"


class TaxSerializer(serializers.ModelSerializer):
    # Income=IncomeSerializer(required=False)
    class Meta:
        model = Tax
        fields ="__all__"

       
    
    