from . import views
from django.urls import path
from gym import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('pt_booking/', views.set_up_personal_training_page),
    path('create_personal_training_session',
         views.create_personal_training_session),
]
