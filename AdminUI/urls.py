from django.urls import path
from . import views
from .views import AdminLoginView

app_name = 'adminUI'

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='login'),
    path('', views.adminUI, name='adminUI'),
]
