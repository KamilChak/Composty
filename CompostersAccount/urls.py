from django.urls import path
from . import views

urlpatterns = [
    path('CR/', views.composterSignup, name='composterSignup'),
    path('CL/', views.composterLogin, name='composterLogin'),
    path('home/', views.composterHome, name='composterHome'),
    path('calendar/', views.composterCalendar, name="composterCalendar"),
    path('GreenersRequest/', views.composterGreenersRequest, name='composterGreenersRequest'),
    path('confirm_offer/<int:offer_id>/', views.confirm_offer, name='confirm_offer'),
    path('logout/', views.logoff , name='logoff'),
]