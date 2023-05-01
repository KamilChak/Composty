from django.urls import path
from . import views

urlpatterns = [
    path('GR/', views.greenerSignup, name='greenerSignup'),
    path('GL/', views.greenerLogin, name='greenerLogin'),
    path('home/', views.greenerHome, name='greenerHome'),
    path('offer/', views.compostOffer, name='compostOffer'),
    path('get_closest_composters/', views.getClosestComposters, name='getClosestComposters'),
    path('send_requests/', views.sentRequests, name='sentRequests'),
    path('logout/', views.logoff , name='logoff'),
]