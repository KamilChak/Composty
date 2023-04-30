from django.urls import path
from . import views

urlpatterns = [
    path('CR/', views.composterSignup, name='composterSignup'),
    path('CL/', views.composterLogin, name='composterLogin'),
    path('home/', views.composterHome, name='composterHome'),
    path('calendar/', views.composterCalendar, name="composterCalendar"),
    path('GreenersRequest/', views.composterGreenersRequest, name='composterGreenersRequest'),
    path('logout/', views.logoff , name='logoff'),
]