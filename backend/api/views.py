import os
# Django
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.db import transaction, IntegrityError
from django.core.mail import EmailMessage
from email.utils import formataddr
from email.mime.image import MIMEImage
from django.db.models import Prefetch

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Other
from api.models import *
from api.serializer import *
from api.utils import *
from datetime import datetime
import json
import imghdr
import traceback

def root(request):
    return HttpResponse("<h1>Aivise Health</h1>")


@api_view(['GET'])
def get_current_server_time(request):
    return Response({'timestamp': timezone.now().timestamp(), 'current_date': timezone.now().date()}, status=200)


@api_view(['POST'])
def refresh_server(request):
    return Response(status=200)


# LOGIN
class UserAuthSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        return token


class UserAuthView(TokenObtainPairView):
    serializer_class = UserAuthSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        if refresh_token:
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.DEBUG is False,
                samesite="Lax" if settings.DEBUG else "None",
                path="/",
            )
            del response.data['refresh']

        return response


# Refresh Token
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            raise AuthenticationFailed("You have been logged out")

        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)
    
        if response.status_code == 200:
            new_refresh_token = response.data['refresh']
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=settings.DEBUG is False,
                samesite="Lax" if settings.DEBUG else "None",
                path="/",
                expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            )
            del response.data['refresh']

        return response


# Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'message': 'Missing refresh token'}, status=401)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        return Response({'message': 'Invalid refresh token'}, status=400)
    
    response = Response(status=200)
    response.delete_cookie("refresh_token", path="/")
    return response


# User Data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    role = request.GET.get('role')
    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'last_login': user.last_login,
        'email': user.email,
    }
    current_year = timezone.now().year
    user_data['current_year_start_date'] = datetime(current_year, 1, 1).strftime("%Y-%m-%d")
    user_data['current_year_end_date'] = datetime(current_year, 12, 31).strftime("%Y-%m-%d")
    
    if role.lower() == 'staff':
        try:
            staff = Staff.objects.get(user=user)
            staff_data = StaffSerializer(staff).data
            user_data.update(staff_data)
            user_data['role'] = 'staff'

        except Staff.DoesNotExist:
            return Response({'message': "Invalid credentials"}, status=401)
    
    elif role.lower() == 'client':
        try:
            client = Client.objects.get(user=user)
            client_data = ClientSerializer(client).data
            user_data.update(client_data)
            user_data['role'] = 'client'
        except Client.DoesNotExist:
            return Response({'message': "Invalid credentials"}, status=401)
    else:
        return Response({'message': "Invalid credentials"}, status=401)
        
    return Response(user_data, status=200)


@api_view(['POST'])
def register_client(request):
    data = request.data
    client_data = json.loads(data.get('dataObject'))
    first_name = client_data.get('firstName').strip().title()
    last_name = client_data.get('lastName').strip().title()
    gender = client_data.get('gender')
    age = int(client_data.get('age'))
    contact_one = client_data.get('contactOne').strip().replace(' ', '').replace('  ', '')
    password = client_data.get('password').strip()
    address = client_data.get('address').strip() if client_data.get('address') and client_data.get('address') != 'null' else None
    email = client_data.get('email').strip()
    img = request.FILES.get('img') if data['img'] and data['img'] != 'null' else None
    nationality = client_data.get('nationality').strip()
    allergies = client_data.get('allergies').strip().split(',') if client_data.get('allergies') and client_data.get('allergies') != 'null' else []
    health_conditions = client_data.get('healthConditions').strip().split(',') if client_data.get('healthConditions') and client_data.get('healthConditions') != 'null' else []
    if img and not imghdr.what(img):
        return Response({'message': f"Invalid image! Check the photo you uploaded"}, status=400)
    
    if not valid_email(email):
        return Response({'message': f"{email} is not a valid email. Check your email address"}, status=400)

    if not valid_phone_number(contact_one):
        return Response({"message": f"{contact_one} is not a valid phone number. Check your primary phone number and ensure you omit any leading zero (0) and include the country code instead. For example, use +233596021383 instead of 0596021383."}, status=400)
    with transaction.atomic():
        try:
            user = User.objects.create_user(
                username=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            item_to_create = Client.objects.create(
                user=user,
                gender=gender,
                age=age,
                contact_one=contact_one,
                allergies=[x.strip() for x in allergies],
                health_conditions=[x.strip() for x in health_conditions],
                address=address,
                nationality=nationality,
            )
            item_to_create.img = ClientImageFile.objects.create(filename=img.name, url=img, client=item_to_create) if img else None
            item_to_create.save()
        except IntegrityError:
            transaction.set_rollback(True)
            if img:
                delete_file(img)
            return Response({'message': f"A user with this details already exists."}, status=400)
        except Exception:
            transaction.set_rollback(True)
            if img:
                delete_file(img)
            log_error(traceback.format_exc())
            return Response(status=400)
        
    # Send mail
    business_logo_link = """<p><img src="cid:logo" alt="Company Logo" /></p>"""
    body = f"""
        <div style="font-size: 16px; font-family: Arial, sans-serif; color: #333;">
            Hi {first_name},
            <p>Welcome to <strong>Aivise Health</strong> — where cutting-edge technology meets quality care!</p>
            <p>We're excited to have you on board. Aivise Health is redefining healthcare with the power of AI — offering smarter consultations, personalized recommendations, and easy access to trusted professionals, all from the comfort of your device.</p>
            <p>Your account is now active! You can explore features like online consultations, our e-pharmacy, dietetic support, and more.</p>
            <p>Need help or have questions? Our support team is always here for you.</p>
            <p>To better health, smarter care, and a brighter future,</p>
            <p><em>— The Aivise Health Team</em></p>
            {business_logo_link}
        </div>
    """
    email_subject = f"🤖 Your AI-Powered Health Journey Begins Now!"
    email_sender = formataddr((os.environ.get('EMAIL_SENDER_NAME'), os.environ.get('EMAIL_HOST_USER')))
    try:
        send_email = EmailMessage(email_subject, body, email_sender, to=[user.email])
        logo_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'images', 'ai_impact.png')
        if logo_path:
            with open(logo_path, 'rb') as logo_file:
                logo_image = MIMEImage(logo_file.read())
                logo_image.add_header('Content-ID', '<logo>')
                send_email.attach(logo_image)
        send_email.content_subtype = "html"
        send_email.send(fail_silently=False)
    except Exception:
        log_error(traceback.format_exc())

    return Response({'username': email, 'password': password}, status=200)
