from pathlib import Path
from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from backend.production import ALLOWED_HOSTS
from api.models import *

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTION_DOMAIN = ALLOWED_HOSTS[0]

def get_default_image(default_img:str=''):
    if default_img == 'staff_img':
        default_img = 'staff_img.jpg'
    elif default_img == 'business_logo':
        default_img = 'business_logo.png'
    
    img = ''
    if settings.DEBUG:
        img = f"http://localhost:8000/static/images/{default_img}"
    else:
        img = f"https://{PRODUCTION_DOMAIN}/static/images/{default_img}"
    
    return img


def get_file_url(data, property_reference):
    url = data[property_reference]
    if settings.DEBUG:
        if url and url != 'null':
            url = f"http://localhost:8000{url}"
    
    return url


class StaffImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffImageFile
        fields = ('url', 'filename', 'id')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['url'] = get_file_url(data, 'url')
        
        return data
    

class ClientImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientImageFile
        fields = ('url', 'filename', 'id')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['url'] = get_file_url(data, 'url')
        
        return data


# Staff Serializers
class StaffSerializer(serializers.ModelSerializer):
    img = StaffImageFileSerializer()

    class Meta:
        model = Staff
        exclude = ["user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['img']:
            data['img'] = get_default_image('staff_img')
               
        return data


class StaffSerializerOne(serializers.ModelSerializer):
    img = StaffImageFileSerializer()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ['user', 'gender', 'age', 'contact_one', 'nationality', 'img', 'bio', 'languages', 'years_of_experience', 'specialization']

    def get_user(self, obj):
        return f"Dr. {obj.user.first_name} {obj.user.last_name}"


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['img']:
            data['img'] = get_default_image('staff_img')
               
        return data
    

# Client Serializers
class ClientSerializer(serializers.ModelSerializer):
    img = StaffImageFileSerializer()

    class Meta:
        model = Client
        exclude = ["user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['img']:
            data['img'] = get_default_image('staff_img')
               
        return data


# Consultation Serializers
class ConsultationSerializerOne(serializers.ModelSerializer):
    staff = StaffSerializerOne()
    follow_up = serializers.SerializerMethodField()
    
    class Meta:
        model = Consultation
        exclude = ["client"]
    
    def get_follow_up(self, obj):
        return {
            'id': obj.follow_up.id,
            'name': obj.follow_up.name,
        }  if obj.follow_up else None


# Drug Serializers
class DrugSerializerOne(serializers.ModelSerializer):
    stocks = serializers.SerializerMethodField()
    
    class Meta:
        model = Drug
        exclude = ["created_at"]
    
    def get_stocks(self, obj):
        return [{
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'price': float(item.price) * 10,
            'is_prescription_required': item.is_prescription_required,
        } for item in obj.stocks.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_file_url(data, 'img')
        
        return data


# Drug Stock Serializers
class DrugStockSerializerOne(serializers.ModelSerializer):    
    class Meta:
        model = DrugStock
        fields = ["name", "price", "quantity"]


# Order Serializers
class OrderSerializerOne(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        exclude = ["client"]
    
    def get_items(self, obj):
        return [{
            'id': item.id,
            'drug': {'id': item.drug.id, 'name': item.drug.name},
            'quantity': item.quantity,
            'price': item.price,
            'total_price': item.total_price,
        } for item in obj.items.all()]


# Message Serializers
class MessageSerializerOne(serializers.ModelSerializer): 
    class Meta:
        model = Message
        fields = ('id', 'sender', 'message')


# Diet Plan Serializers
class DietPlanSerializerOne(serializers.ModelSerializer): 
    class Meta:
        model = DietPlan
        exclude = ["client"]