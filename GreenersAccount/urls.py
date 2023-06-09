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
    path('GreenerHomeChooseComposter/', views.greenerHomeChooseComposter, name='greenerHomeChooseComposter'),
    path('GreenerRequestComposterLink/', views.greenerRequestComposterLink, name='greenerRequestComposterLink'),
    path('GreenerNotification', views.greenerNotification, name='greenerNotification'),
    path('deleteNotification/<int:notif_id>/', views.deleteNotification, name='deleteNotification'),
    path('update_composter/', views.updateComposter, name ='updateComposter'),
    path('checkEmail/', views.checkEmail, name="checkEmail"),
]