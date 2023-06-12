from . import views
from django.urls import path
from gym import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('pt_booking/', views.set_up_personal_training_page),
    path('create_personal_training_session',
         views.create_personal_training_session),
    path('delete_personal_training_session',
         views.delete_personal_training_session),
    path('update_personal_training_session',
         views.update_personal_training_session),
]
