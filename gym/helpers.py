"""
    Helper functions that are used in the gym/view.py file
"""
from .models import PersonalTraining
from datetime import datetime


def book_personal_training(user, datetime):
    personal_training_object = PersonalTraining.objects.create(
        date_time=datetime, booked_by=user)
    personal_training_object.save()
    return personal_training_object


# '2023-06-14'
def is_date_later_than_or_equal_to_todays_date(date):
    todaysDate = datetime.today()
    return date.date() >= todaysDate.date()


def format_datetime(date, time):
    format_data = "%Y-%m-%d %H:%M:%S"
    formatted_date = f"{date} {time}:00"
    date_time = datetime.strptime(formatted_date, format_data)
    return date_time


# June 28, 2023, 7 a.m.
def convert_datetime_for_display(datetime):
    return f"{datetime.strftime('%B')} {datetime.day}, \
        {datetime.year}, {datetime.hour}:00 "


# Parameter ex.: June 28, 2023, 7 a.m., Parameter example: June 28, 2023, noon
def convert_date_time(date_time):
    CONVERT_AM_PM = {"p.m.": "PM", "a.m.": "AM"}
    convert = date_time.split(" ")
    # This value is noon if not a.m. or p.m.
    if convert[-1] not in CONVERT_AM_PM:
        convert[-1] = '12PM'
    else:
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


def update_personal_training(user, current_datetime, new_datetime):
    try:
        current_training_session = PersonalTraining.objects.get(
            booked_by=user, date_time=current_datetime)

        primary_key = current_training_session.pk

        personal_training_object = PersonalTraining.objects.filter(
            pk=primary_key, booked_by=user, date_time=current_datetime).update(
            date_time=new_datetime)
    except PersonalTraining.DoesNotExist:
        return {}
    return personal_training_object


def get_personal_training_sessions(user):
    personal_trainings = PersonalTraining.objects.filter(
        booked_by=user)

    return personal_trainings


def get_future_personal_training_sessions(user):
    personal_trainings = PersonalTraining.objects.filter(
        booked_by=user, date_time__gt=datetime.today())

    return personal_trainings
