import os
from datetime import datetime, timedelta
import google.generativeai as genai

# django
from django.core.validators import EmailValidator
from django.conf import settings
from django.http import FileResponse

import phonenumbers
from phonenumbers import NumberParseException
import pusher
from timezonefinder import TimezoneFinder
import pytz
from haversine import haversine, Unit
import logging
import secrets
import string
import requests
import io


# Base url
def base_url(value):
    scheme = value.scheme
    host = value.get_host()
    return f"{scheme}://{host}"


def valid_phone_number(number:str):
    try:
        phone_number = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(phone_number):
            return False
    except NumberParseException:
        return False
    return True

def valid_email(email:str):
    email_validator = EmailValidator()
    try:
        email_validator(email)
    except Exception:
        return False
    return True


def generate_temp_password(length=12):
    letters_digits = string.ascii_letters + string.digits
    symbols = "&#@$%"
    characters = letters_digits + symbols
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def log_error(error_message:str):
    logging.basicConfig(filename='error.log', level=logging.INFO)
    logging.info(error_message)


def use_pusher():
    pusher_client = pusher.Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_KEY,
        secret=settings.PUSHER_SECRET,
        cluster=settings.PUSHER_CLUSTER,
    )
    return pusher_client


class ErrorMessageException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    def __str__(self) -> str:
        return self.message 


# Convert datetime
def format_relative_date_time(utc_date, day_name, time):
    # Convert the UTC string to a datetime object
    utc_datetime = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Get the current UTC datetime
    current_utc_datetime = datetime.now()

    # Check if it's today
    if utc_datetime.date() == current_utc_datetime.date():
        if day_name and time:
            return f"Today, {utc_datetime.strftime('%B %d, %Y at %H:%M')}"
        elif day_name and not time:
            return f"Today, {utc_datetime.strftime('%B %d, %Y')}"
        elif not day_name and time:
            return utc_datetime.strftime('%B %d, %Y at %H:%M')
        elif not day_name and not time:
            return utc_datetime.strftime('%B %d, %Y')

    elif utc_datetime.date() == (current_utc_datetime - timedelta(days=1)).date():
        if day_name and time:
            return f"Yesterday, {utc_datetime.strftime('%B %d, %Y at %H:%M')}"
        elif day_name and not time:
            return f"Yesterday, {utc_datetime.strftime('%B %d, %Y')}"
        elif not day_name and time:
            return utc_datetime.strftime('%B %d, %Y at %H:%M')
        elif not day_name and not time:
            return utc_datetime.strftime('%B %d, %Y')

    else:
        if day_name and time:
            return utc_datetime.strftime('%A, %B %d, %Y at %H:%M')
        elif day_name and not time:
            return utc_datetime.strftime('%A, %B %d, %Y')
        elif not day_name and time:
            return utc_datetime.strftime('%B %d, %Y at %H:%M')
        elif not day_name and not time:
            return utc_datetime.strftime('%B %d, %Y')


def is_within_radius(user_lat, user_lon, office_lat, office_lon, radius_m):
    user_location = (user_lat, user_lon)
    office_location = (office_lat, office_lon)
    distance_m = haversine(user_location, office_location, unit=Unit.METERS)

    return distance_m <= radius_m


def get_timezone(lat:float, lon:float):
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=lon, lat=lat)
    return timezone


def convert_to_local_datetime(utc_datetime, user_timezone):
    user_tz = pytz.timezone(user_timezone)
    return utc_datetime.replace(tzinfo=pytz.utc).astimezone(user_tz)


def get_current_user_utc_datetime(user_timezone):
    user_tz = pytz.timezone(user_timezone)
    user_local_time = datetime.now(user_tz)
    utc_datetime = user_local_time.astimezone(pytz.utc)
    return utc_datetime


def get_currency_exchange_rate(base_currency, target_currency):
    api_key = os.environ.get('EXCHANGE_RATE_API_KEY')
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    data = response.json()
    return data['conversion_rate']


def delete_file(File):
    if hasattr(File, 'url') and hasattr(File.url, 'name') and hasattr(File.url, 'storage'):
        storage = File.url.storage
        path = File.url.name
        if storage.exists(path):
            storage.delete(path)


def send_file(file_type:str, byte_file:io.BytesIO, filename:str):
    byte_file.seek(0)
    if file_type == 'excel':
        filename += '.xlsx'
        response = FileResponse(byte_file, as_attachment=True, filename=filename)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif file_type == 'pdf':
        filename += '.pdf'
        response = FileResponse(byte_file, as_attachment=True, filename=filename)
        response['Content-Type'] = 'application/pdf'
    elif file_type == 'png':
        filename += '.png'
        response = FileResponse(byte_file, as_attachment=True, filename=filename)
        response['Content-Type'] = 'image/png'
    else:
        raise Exception('Invalid file type')
    
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response


def send_prompt_to_gemini(message):
    api_key = os.environ.get('GEMINI_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(message)

    return response.text