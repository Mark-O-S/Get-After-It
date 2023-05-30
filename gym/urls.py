from . import views
from django.urls import path
from gym import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('gym_booking/', views.get_personal_training_sessions),
]
