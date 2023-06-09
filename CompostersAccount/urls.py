from django.urls import path
from . import views

urlpatterns = [
    path('CR/', views.composterSignup, name='composterSignup'),
    path('CL/', views.composterLogin, name='composterLogin'),
    path('home/', views.composterHome, name='composterHome'),
    path('GreenersRequest/', views.composterGreenersRequest, name='composterGreenersRequest'),
    path('confirm_offer/<int:offer_id>/', views.confirm_offer, name='confirm_offer'),
    path('decline_offer/<int:offer_id>/', views.decline_offer, name='decline_offer'),
    path('logout/', views.logoff , name='logoff'),
    path('getPendingMembers/', views.getPendingMembers, name="getPendingMembers"),
    path('removeComposterMember/<int:member_id>/',views.removeComposterMember, name="removeComposterMember"),
    path('accept_greener/',views.acceptGreener, name='acceptGreener'),
    path('reject_greener/',views.rejectGreener, name='rejectGreener'),
    path('offers_data/',views.GreenersOffers, name="GreenersOffers"),
    path('GreenersRequest/', views.getGreenersOffer, name='getGreenersOffer'),
    path('ComposterMembers/', views.getComposterMembers, name='getComposterMembers'),
    path('checkEmail/', views.checkEmail, name="checkEmail"),
]