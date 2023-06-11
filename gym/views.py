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
    datetime_now = datetime.today()
    filter_week_from_today = datetime_now + timedelta(days=WEEK_LONG)

    personal_trainings = PersonalTraining.objects.filter(
        booked_by=user, date_time__gt=datetime_now,
        date_time__lt=filter_week_from_today)

    return personal_trainings


def book_personal_training(request):
    if request.method == 'GET':
        user = request.user
        return user

    # Check if the date time is available
    # personal_trainings = PersonalTraining.objects.filter(
    #     booked_by=user, date_time)

    # Check if the date time is available
    # PersonalTraining.objects.create(
    #     subject=subject + ": " + user_profile.get_full_name(),
    #     message=body,
    #     user=user_profile)


def set_up_personal_training_page(request):

    # Get all pt sessions that are on the current day and for the next 7 days
    # This is for displaying the booked sessions upcoming for the next 7 days
    # personal_training_sessions = get_personal_training_sessions(
    #     request.user)

    # Have to create a range value since it doesn't exist in template django
    context = {
        'times_list': TIMES_LIST
    }
    return render(request, "pt_booking.html", context)

def update_personal_training_session(request):
    # Try and book a session
    booked_session = book_personal_training(request)

    if request.method == 'GET':  # If the form has been submitted...
        form = request.GET  # A form bound to the POST data
        personal_training_date = form["personal_training_date"]
        time = form["times_list"]
        booking_status = "There is an issue"

        format_data = "%Y-%m-%d %H:%M:%S"
        personal_training_date = f"{personal_training_date} {time}:00"
        filter_datetime = datetime.strptime(personal_training_date,
                                            format_data)

        personal_training_data = {}
        # Check if the date and time user chose is available
        try:
            personal_training_data = PersonalTraining.objects.get(
                date_time__date=filter_datetime.date(),
                date_time__hour=filter_datetime.hour)
            personal_training_data = {personal_training_data}
        except PersonalTraining.DoesNotExist:
            booking_status = "This session is available"

        if len(personal_training_data) > 0:
            session_message = "This session is not available"
            messages.add_message(request, messages.ERROR, session_message)
            context = {
                'booking_status': booking_status,
                'session_message': session_message,
                'times_list': TIMES_LIST
            }
            return render(request, "pt_booking.html", context)

        context = {
            'booking_status': session_message,
            'booking_date': personal_training_data,
            'time': time
        }
        return render(request, "pt_booking_session.html", context)
