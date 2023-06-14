from django.shortcuts import render
from .models import PersonalTraining
from datetime import datetime, timedelta
from django.contrib import messages


TIMES = {f"{time}": "test" for time in range(7, 22)}
TIMES_LIST = [f"{time}:00" for time in range(7, 22)]
CONVERT_AM_PM = {"p.m.": "PM", "a.m.": "AM"}
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

    if request.method == 'GET':
        # Get all pt sessions that the user booked
        personal_training_booked_sessions = get_personal_training_sessions(
            request.user)

        context = {
            'times_list': TIMES_LIST,
            'booked_sessions': personal_training_booked_sessions,
            'session_message': ""
        }
        return render(request, "pt_booking.html", context)


def book_personal_training(user, datetime):
    personal_training_object = PersonalTraining.objects.create(
        date_time=datetime, booked_by=user)
    personal_training_object.save()
    return personal_training_object


def update_personal_training(user, current_datetime, new_datetime):
    try:
        current_training_session = PersonalTraining.objects.get(
            booked_by=user, date_time=current_datetime)

        primary_key = current_training_session.pk

        personal_training_object = PersonalTraining.objects.filter(
            pk=primary_key, booked_by=user, date_time=current_datetime).update(
            date_time=new_datetime)
    except:
        return {}
    return personal_training_object


def format_datetime(date, time):
    format_data = "%Y-%m-%d %H:%M:%S"
    formatted_date = f"{date} {time}:00"
    date_time = datetime.strptime(formatted_date, format_data)
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


# Parameter example: June 28, 2023, 7 a.m.
def convert_date_time(date_time):
    convert = date_time.split(" ")
    am_pm = CONVERT_AM_PM[convert[-1]]
    convert[-1] = am_pm
    date_time = "".join(convert)

    datetime_object = datetime.strptime(date_time, "%B%d,%Y,%I%p")
    return datetime_object


# Parameter example: June 28, 2023, 7 a.m.
def convert_date_time_with_new_time(date_time, new_time):
    convert = date_time.split(",")
    formatted_new_time = f"{new_time}:00"
    convert[-1] = formatted_new_time
    date_time = "".join(convert)
    datetime_object = datetime.strptime(date_time, "%B %d %Y%X")
    return datetime_object


def delete_personal_training_session(request):
    if request.GET:
        form = request.GET
        date_time = form["delete_session"]
        converted_date_time = convert_date_time(date_time)
        PersonalTraining.objects.filter(date_time=converted_date_time).delete()

        session_message = "Personal Training Session successfully deleted"
        messages.add_message(request, messages.INFO, session_message)
        context = {
            'session_message': session_message,
            'booking_status': session_message,
            'time': date_time,
        }
        return render(request, "pt_delete_session.html", context)


# Check if the user is trying to book the same time, return error is yes
# Check if the new time is available to book, return error if not
# Check if the new time is available to book, return success if yes
def update_personal_training_session(request):
    personal_training_booked_sessions = get_personal_training_sessions(
        request.user)
    if request.GET:
        form = request.GET
        current_booking_datetime = form["current_times_list"]
        new_time = form["edit_times_list"]
        personal_training_data = {}
        session_message = ""
        redirect_url = "pt_booking.html"
        new_datetime = convert_date_time_with_new_time(
            current_booking_datetime, new_time)
        converted_current_date_time = convert_date_time(
            current_booking_datetime)

        converted_current_hour = converted_current_date_time.hour
        current_time = f"{converted_current_hour}:00"
        # If the current time and new time match, no update happens - exit early
        if current_time == new_time:
            session_message = "This session is already booked"
            messages.add_message(request, messages.INFO, session_message)
            context = {
                'session_message': session_message,
                'booking_status': session_message,
                'times_list': TIMES_LIST,
                'personal_training_data': personal_training_data,
                'booked_sessions': personal_training_booked_sessions
            }
            return render(request, redirect_url, context)

        # Get the date from the current booking and use that to search if that
        # date and new time are available
        # Check if the date and time user chose is available
        try:
            personal_training_data = PersonalTraining.objects.get(
                date_time=new_datetime)
            personal_training_data = {personal_training_data}
            session_message = f"This session is not available to book {new_datetime} {personal_training_data}"
            messages.add_message(request, messages.ERROR, session_message)
        except PersonalTraining.DoesNotExist:
            # Session is available to book for the user

            # Update the current personal training object with new date time
            booked_session = update_personal_training(
                request.user, converted_current_date_time, new_datetime)
            personal_training_data = {booked_session}
            session_message = "Personal Training Session successfully updated"
            messages.add_message(request, messages.INFO, session_message)
            redirect_url = "pt_update_session.html"

        context = {
            'session_message': session_message,
            'booking_status': session_message,
            'times_list': TIMES_LIST,
            'personal_training_data': personal_training_data,
            'booked_sessions': personal_training_booked_sessions,
        }
        return render(request, redirect_url, context)
