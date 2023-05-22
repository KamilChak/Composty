from django.urls import path
from . import views
from .views import AdminLoginView, AdminLogoutView

app_name = 'adminUI'

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='login'),
    path('logout/', AdminLogoutView.as_view(), name='logout'),
    path('', views.adminUI, name='adminUI'),
    path('map/', views.google_maps, name='map'),
]
