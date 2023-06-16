from django.shortcuts import render
from .models import PersonalTraining
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .helpers import *


TIMES_LIST = [f"{time}:00" for time in range(7, 22)]


def Home(request):
    return render(request, "index.html")


@login_required
def set_up_personal_training_page(request):
    if request.method == 'GET':
        # Get all personal training sessions that the user booked
        personal_training_booked_sessions = get_personal_training_sessions(
            request.user)

        context = {
            'times_list': TIMES_LIST,
            'booked_sessions': personal_training_booked_sessions,
            'session_message': ""
        }
        return render(request, "pt_booking.html", context)


def create_personal_training_session(request):
    personal_training_booked_sessions = get_personal_training_sessions(
        request.user)

    if request.method == 'GET':  # If the form has been submitted...
        form = request.GET  # A form bound to the POST data
        personal_training_date = form["personal_training_date"]
        time = form["times_list"]
        filter_datetime = format_datetime(personal_training_date, time)
        redirect_url = "pt_booking.html"

        context = {
            "personal_training_data": {},
            "session_message": "",
            "date_message": "",
            "times_list": TIMES_LIST,
            "time": time,
            "booked_sessions": personal_training_booked_sessions
        }

        isDateLater = is_date_later_than_or_equal_to_todays_date(filter_datetime)
        if isDateLater is False:
            context["session_message"] = "Please choose today's date or a \
                                later date to book."
            messages.add_message(request, messages.ERROR, context["session_message"])
            return render(request, redirect_url, context)

        # Check if the date and time user chose is available
        try:
            personal_training_data = PersonalTraining.objects.get(
                date_time__date=filter_datetime.date(),
                date_time__hour=filter_datetime.hour)
            context["personal_training_data"] = {personal_training_data}
            context["session_message"] = "This session is not available"
            messages.add_message(request, messages.ERROR, session_message)
        except PersonalTraining.DoesNotExist:
            # Session is available to book for the user
            booked_session = book_personal_training(request.user,
                                                    filter_datetime)
            context["personal_training_data"] = {booked_session}
            context["session_message"] = "Personal Training Session successfully booked!"
            context["date_message"] = booked_session.date_time
            messages.add_message(request, messages.INFO, context["session_message"])
            redirect_url = "pt_booking_session.html"

        return render(request, redirect_url, context)


@login_required
def delete_personal_training_session(request):
    if request.GET:
        form = request.GET
        date_time = form["delete_session"]
        converted_date_time = convert_date_time(date_time)
        PersonalTraining.objects.filter(date_time=converted_date_time).delete()

        session_message = "Personal Training Session successfully deleted!"
        messages.add_message(request, messages.INFO, session_message)
        context = {
            'session_message': session_message,
            'time': date_time,
            'date_message': date_time
        }
        return render(request, "pt_booking_session.html", context)


# Check if the user is trying to book the same time, return error is yes
# Check if the new time is available to book, return error if not
# Check if the new time is available to book, return success if yes
@login_required
def update_personal_training_session(request):
    personal_training_booked_sessions = get_personal_training_sessions(
        request.user)
    if request.GET:
        form = request.GET
        current_booking_datetime = form["current_times_list"]
        new_time = form["edit_times_list"]
        redirect_url = "pt_booking.html"
        
        context = {
            "session_message": "",
            "personal_training_data": {},
            "date_message": "",
            "times_list": TIMES_LIST,
            "booked_sessions": personal_training_booked_sessions
        }
        
        new_datetime = convert_date_time_with_new_time(
            current_booking_datetime, new_time)
        converted_current_date_time = convert_date_time(
            current_booking_datetime)
        converted_current_hour = converted_current_date_time.hour
        current_time = f"{converted_current_hour}:00"

        # If current time and new time match, no update happens - exit early
        if current_time == new_time:
            context["session_message"] = "This session is already booked"
            context["session_message"] = session_message,
            messages.add_message(request, messages.INFO, context["session_message"])
            return render(request, redirect_url, context)

        # Get the date from the current booking and use that to search if that
        # date and new time are available
        # Check if the date and time user chose is available
        try:
            personal_training_data = PersonalTraining.objects.get(
                date_time=new_datetime)
            context["personal_training_data"] = {personal_training_data}
            context["session_message"] = f"The session time {new_time} is not available to book"
            messages.add_message(request, messages.ERROR, context["session_message"])
        except PersonalTraining.DoesNotExist:
            # Session is available to book for the user

            # Update the current personal training object with new date time
            booked_session = update_personal_training(
                request.user, converted_current_date_time, new_datetime)
            context["personal_training_data"] = {booked_session}
            context["date_message"] = convert_datetime_for_display(new_datetime)
            context["session_message"] = "Personal Training Session successfully updated!"
            redirect_url = "pt_booking_session.html"
            messages.add_message(request, messages.INFO, context["session_message"])

        return render(request, redirect_url, context)
