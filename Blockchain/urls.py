from django.urls import path
from . import views


urlpatterns = [
    #path('transaction/', views.transaction, name='transaction'),
    path('', views.display_chain, name='get_chain'),
    path('nodes/', views.display_nodes, name='get_chain'),
]