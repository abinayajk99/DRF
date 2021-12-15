

# Create your models here

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class CompanyProfile(models.Model):
    company_name=models.CharField(max_length=100,blank=True)
    company_grade=models.CharField(max_length=10,blank=True)
    address=models.CharField(max_length=100,blank=True)
    designation=models.CharField(max_length=100,blank=True)
    salary= models.DecimalField(max_digits=6, decimal_places=2,blank=True)

    class Meta:
        app_label='restapi_app'

    

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("-","-"),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,default="-")
    aboutme = models.CharField(max_length=100, default='')
    age = models.CharField(max_length=2,default='')
    company_profile=models.ForeignKey(CompanyProfile,related_name='company_profile', on_delete=models.CASCADE,blank=True,null=True)
    is_delete = models.BooleanField(default=True)
    
    class Meta:
        app_label='restapi_app'

