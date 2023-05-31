from django.shortcuts import render
from .models import PersonalTraining

def Home(request):

    return render(request, "index.html")

def get_personal_training_sessions(request):
    personal_trainings = PersonalTraining.objects.all()
    context = {
        'personal_trainings': personal_trainings
    }
    return render(request, "gym_booking.html", context)
