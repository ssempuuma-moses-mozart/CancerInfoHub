from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # path('', views.home, name='partners-home'),

    path('donate/',views.donate,name='donate'),
  
]