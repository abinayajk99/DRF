from djongo import models
from django import forms
from django.contrib.auth.models import User
from datetime import *



# class Income(models.Model):
    
#     income_options=[
#         ("-","-"),
#         ("sales","sales"),
#         ("commisions","commisions")
#     ]
#     income_category = models.CharField(max_length=20,choices=income_options,default="-",blank=True,null=True)
#     date =models.DateField(blank=True,null=True)
#     description =models.CharField(max_length=200,blank=True,null=True)
#     amount = models.IntegerField(blank=True,null=True)
    
#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.income_category

# class IncomeForm(forms.ModelForm):
#     class Meta:
#         model = Income
#         fields = ('income_category', 'date','description','amount')
    

# class Expense(models.Model):
  
#     expense_choice=[
#         ("-","-"),
#         ("travel","travel"),
#         ("rent","rent")
#     ]
#     expense_title=models.CharField(max_length=100,choices=expense_choice,default="-",blank=True,null=True)
#     expense_category=models.CharField(max_length=100,blank=True,null=True)
#     date=models.DateField(blank=True,null=True)
#     description =models.CharField(max_length=100,blank=True,null=True)
#     amount = models.IntegerField(blank=True,null=True)

#     # class Meta:
#     #     abstract = True

# class ExpenseForm(forms.ModelForm):
#     class Meta:
#         model = Expense
#         fields = ('expense_title', 'expense_category','date','description','amount')

class Tax(models.Model):
   
    user_id= models.IntegerField()
    category_choice=[
        ("-","-"),
        ("self-employeed","self-employeed"),
        ("employeed","employeed"),
    ]
    title=models.CharField(max_length=20,choices=category_choice,default="-")
    date=models.DateField(blank=True,null=True)
    description=models.CharField(max_length=255,blank=True,null=True)
    Amount=models.IntegerField()
    Income = models.CharField(max_length=255,blank=True,null=True)
    Expense =models.CharField(max_length=255,blank=True,null=True)
    # objects = models.DjongoManager()

    class Meta:
        app_label = 'tax'

    def __str__(self):
        return self.title







