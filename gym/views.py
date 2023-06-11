from django.shortcuts import render
from .models import PersonalTraining
from datetime import datetime, timedelta
from django.contrib import messages


TIMES = {f"{time}": "test" for time in range(7, 22)}
TIMES_LIST = [f"{time}:00" for time in range(7, 22)]
WEEK_LONG = 7


def Home(request):
    return render(request, "index.html")


# Set up personal training week
def set_up_pt_week():
    pt_week = {}
    datetime_now = datetime.today()

    # Get all datetimes from today to the next 7 days
    week_from_today = [datetime_now +
                       timedelta(days=num) for num in range(WEEK_LONG)]

    # Get all dates from today to the next 7 days and set times as the value
    for day in week_from_today:
        pt_week[day.date()] = TIMES
    return pt_week


def get_personal_training_sessions(user):
    personal_trainings = PersonalTraining.objects.filter(
        booked_by=user)

    return personal_trainings


def set_up_personal_training_page(request):

    # Get all pt sessions that the user booked
    personal_training_booked_sessions = get_personal_training_sessions(
        request.user)

    # Have to create a range value since it doesn't exist in template django
    context = {
        'times_list': TIMES_LIST,
        'booked_sessions': personal_training_booked_sessions
    }
    return render(request, "pt_booking.html", context)


def book_personal_training(user, datetime):
    personal_training_object = PersonalTraining.objects.create(
        date_time=datetime, booked_by=user)
    personal_training_object.save()
    return personal_training_object


def format_datetime(date, time):
    format_data = "%Y-%m-%d %H:%M:%S"
    formatted_date = f"{date} {time}:00"
    date_time = datetime.strptime(formatted_date,
                                  format_data)
    return date_time


def create_personal_training_session(request):
    personal_training_booked_sessions = get_personal_training_sessions(
        request.user)

    if request.method == 'GET':  # If the form has been submitted...
        form = request.GET  # A form bound to the POST data
        personal_training_date = form["personal_training_date"]
        time = form["times_list"]
        filter_datetime = format_datetime(personal_training_date, time)

        personal_training_data = {}
        session_message = ""
        redirect_url = "pt_booking.html"

        # Check if the date and time user chose is available
        try:
            personal_training_data = PersonalTraining.objects.get(
                date_time__date=filter_datetime.date(),
                date_time__hour=filter_datetime.hour)
            personal_training_data = {personal_training_data}
            session_message = "This session is not available"
            messages.add_message(request, messages.ERROR, session_message)
        except PersonalTraining.DoesNotExist:
            # Session is available to book for the user
            booked_session = book_personal_training(request.user,
                                                    filter_datetime)
            personal_training_data = {booked_session}
            session_message = "Personal Training Session successfully booked"
            messages.add_message(request, messages.INFO, session_message)
            redirect_url = "pt_booking_session.html"

        context = {
            'session_message': session_message,
            'booking_status': session_message,
            'booking_date': personal_training_data,
            'time': time,
            'times_list': TIMES_LIST,
            'booked_sessions': personal_training_booked_sessions
        }
        return render(request, redirect_url, context)
