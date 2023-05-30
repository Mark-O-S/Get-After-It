from . import views
from django.urls import path
from gym import views

urlpatterns = [
    path('', views.Home, name="Home")
]
