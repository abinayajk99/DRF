from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('<pk>/tax/schedule/',Schedule.as_view() ),
    path('<int:user_id>/tax/schedule/<int:pk>/',ScheduleEdit.as_view()),
]