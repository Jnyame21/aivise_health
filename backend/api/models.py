from django.db import models
import re
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
import math
from django.conf import settings
from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage, VideoMediaCloudinaryStorage

NATIONALITY_CHOICES = [
    ("Afghan", "Afghan"),
    ("Albanian", "Albanian"),
    ("Algerian", "Algerian"),
    ("Andorran", "Andorran"),
    ("Angolan", "Angolan"),
    ("Antiguan", "Antiguan"),
    ("Argentine", "Argentine"),
    ("Armenian", "Armenian"),
    ("Australian", "Australian"),
    ("Austrian", "Austrian"),
    ("Azerbaijani", "Azerbaijani"),
    ("Bahamian", "Bahamian"),
    ("Bahraini", "Bahraini"),
    ("Bangladeshi", "Bangladeshi"),
    ("Barbadian", "Barbadian"),
    ("Belarusian", "Belarusian"),
    ("Belgian", "Belgian"),
    ("Belizean", "Belizean"),
    ("Beninese", "Beninese"),
    ("Bhutanese", "Bhutanese"),
    ("Bolivian", "Bolivian"),
    ("Bosnian", "Bosnian"),
    ("Botswanan", "Botswanan"),
    ("Brazilian", "Brazilian"),
    ("Bruneian", "Bruneian"),
    ("Bulgarian", "Bulgarian"),
    ("Burkinabe", "Burkinabe"),
    ("Burundian", "Burundian"),
    ("Cabo Verdean", "Cabo Verdean"),
    ("Cambodian", "Cambodian"),
    ("Cameroonian", "Cameroonian"),
    ("Canadian", "Canadian"),
    ("Central African", "Central African"),
    ("Chadian", "Chadian"),
    ("Chilean", "Chilean"),
    ("Chinese", "Chinese"),
    ("Colombian", "Colombian"),
    ("Comorian", "Comorian"),
    ("Ivorian", "Ivorian"),
    ("Croatian", "Croatian"),
    ("Cuban", "Cuban"),
    ("Cypriot", "Cypriot"),
    ("Czech", "Czech"),
    ("Congolese", "Congolese"),
    ("Danish", "Danish"),
    ("Djiboutian", "Djiboutian"),
    ("Dominican", "Dominican"),
    ("Ecuadorian", "Ecuadorian"),
    ("Egyptian", "Egyptian"),
    ("Salvadoran", "Salvadoran"),
    ("Equatorial Guinean", "Equatorial Guinean"),
    ("Eritrean", "Eritrean"),
    ("Estonian", "Estonian"),
    ("Eswatini", "Eswatini"),
    ("Ethiopian", "Ethiopian"),
    ("Fijian", "Fijian"),
    ("Finnish", "Finnish"),
    ("French", "French"),
    ("Gabonese", "Gabonese"),
    ("Gambian", "Gambian"),
    ("Georgian", "Georgian"),
    ("German", "German"),
    ("Ghanaian", "Ghanaian"),
    ("Greek", "Greek"),
    ("Grenadian", "Grenadian"),
    ("Guatemalan", "Guatemalan"),
    ("Guinean", "Guinean"),
    ("Bissau-Guinean", "Bissau-Guinean"),
    ("Guyanese", "Guyanese"),
    ("Haitian", "Haitian"),
    ("Honduran", "Honduran"),
    ("Hungarian", "Hungarian"),
    ("Icelandic", "Icelandic"),
    ("Indian", "Indian"),
    ("Indonesian", "Indonesian"),
    ("Iranian", "Iranian"),
    ("Iraqi", "Iraqi"),
    ("Irish", "Irish"),
    ("Israeli", "Israeli"),
    ("Italian", "Italian"),
    ("Jamaican", "Jamaican"),
    ("Japanese", "Japanese"),
    ("Jordanian", "Jordanian"),
    ("Kazakh", "Kazakh"),
    ("Kenyan", "Kenyan"),
    ("Kiribati", "Kiribati"),
    ("Kosovar", "Kosovar"),
    ("Kuwaiti", "Kuwaiti"),
    ("Kyrgyz", "Kyrgyz"),
    ("Lao", "Lao"),
    ("Latvian", "Latvian"),
    ("Lebanese", "Lebanese"),
    ("Basotho", "Basotho"),
    ("Liberian", "Liberian"),
    ("Libyan", "Libyan"),
    ("Liechtensteiner", "Liechtensteiner"),
    ("Lithuanian", "Lithuanian"),
    ("Luxembourger", "Luxembourger"),
    ("Malagasy", "Malagasy"),
    ("Malawian", "Malawian"),
    ("Malaysian", "Malaysian"),
    ("Maldivian", "Maldivian"),
    ("Malian", "Malian"),
    ("Maltese", "Maltese"),
    ("Marshallese", "Marshallese"),
    ("Mauritanian", "Mauritanian"),
    ("Mauritian", "Mauritian"),
    ("Mexican", "Mexican"),
    ("Micronesian", "Micronesian"),
    ("Moldovan", "Moldovan"),
    ("Monegasque", "Monegasque"),
    ("Mongolian", "Mongolian"),
    ("Montenegrin", "Montenegrin"),
    ("Moroccan", "Moroccan"),
    ("Mozambican", "Mozambican"),
    ("Namibian", "Namibian"),
    ("Nauruan", "Nauruan"),
    ("Nepali", "Nepali"),
    ("Dutch", "Dutch"),
    ("New Zealander", "New Zealander"),
    ("Nicaraguan", "Nicaraguan"),
    ("Nigerien", "Nigerien"),
    ("Nigerian", "Nigerian"),
    ("North Macedonian", "North Macedonian"),
    ("Norwegian", "Norwegian"),
    ("Russian", "Russian"),
    ("South African", "South African"),
    ("Korean", "Korean"),
    ("British", "British"),
    ("American", "American"),
]

def staff_folder(instance, filename):
    folder_path =  f"aivise_health/staff/{instance.staff.user.username}/{filename}"
    return folder_path


def client_folder(instance, filename):
    folder_path =  f"aivise_health/clients/{instance.client.user.username}/{filename}"
    return folder_path


class StaffImageFile(models.Model):
    staff = models.ForeignKey("Staff", on_delete=models.SET_NULL, related_name="image_files", null=True)
    url = models.ImageField(verbose_name= 'Image', blank=False, upload_to=staff_folder, null=True, storage=MediaCloudinaryStorage() if not settings.DEBUG else None)
    filename = models.CharField(max_length=255, verbose_name='Filename', blank=False, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff}: {self.filename} : {self.url}"


class ClientImageFile(models.Model):
    client = models.ForeignKey("Client", on_delete=models.SET_NULL, related_name="image_files", null=True)
    url = models.ImageField(verbose_name= 'Image', blank=False, upload_to=client_folder, null=True, storage=MediaCloudinaryStorage() if not settings.DEBUG else None)
    filename = models.CharField(max_length=255, verbose_name='Filename', blank=False, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client}: {self.filename} : {self.url}"


class Staff(models.Model):
    user = models.OneToOneField(User, verbose_name="User", on_delete=models.CASCADE, null=True)
    # Personal Info
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(verbose_name='Gender', max_length=10, choices=gender_choices, blank=True, null=True)
    age = models.IntegerField(verbose_name='Age', blank=True, null=True)
    contact_one = models.CharField(max_length=20, verbose_name='Primary Phone number', blank=False, null=True)
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES, verbose_name='Nationality', null=True)
    img = models.ForeignKey(StaffImageFile, related_name='staff_img', verbose_name='Staff photo', blank=True, null=True, on_delete=models.SET_NULL)
    
    # Professional Info
    specialization = models.CharField(max_length=100, verbose_name="Specialization", blank=True, null=True)
    years_of_experience = models.CharField(max_length=10, verbose_name="Years of Experience", blank=True, null=True)
    languages = models.JSONField(verbose_name='Languages Spoken', blank=True, default=list)
    bio = models.TextField(verbose_name="Short Bio", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date Created")

    def __str__(self):
        return f"{self.user.get_full_name() if self.user else 'Unnamed Staff'}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name="User")
    contact_one = models.CharField(max_length=15, blank=True, null=True, verbose_name="Primary Phone Number")
    age = models.IntegerField(verbose_name='Age', blank=True, null=True)
    address = models.TextField(verbose_name='Residential address', blank=True, null=True)
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES, verbose_name='Nationality', null=True)
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    health_conditions = models.JSONField(verbose_name='Health Conditions', blank=True, default=list)
    allergies = models.JSONField(verbose_name='Allergies', blank=True, default=list)
    img = models.ForeignKey(ClientImageFile, related_name='clients', verbose_name='Client photo', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}" if self.user else 'None'


class Consultation(models.Model):
    TYPE_CHOICES = [
        ('new', 'New Consultation'),
        ('follow_up', 'Follow-up'),
    ]
    name = models.CharField(verbose_name='Name', max_length=200, blank=True, null=True)
    purpose = models.CharField(verbose_name='Purpose', max_length=200, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='consultations')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='consultations')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    follow_up = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='consultations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.client} - {self.staff} - {self.date} {self.time}"
    

class Drug(models.Model):
    name = models.CharField(max_length=200, verbose_name="Drug Name")
    generic_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Generic Name")
    brand = models.CharField(max_length=200, blank=True, null=True, verbose_name="Brand Name")
    description = models.TextField(blank=True, verbose_name="Description")
    dosage_form = models.JSONField(verbose_name='Dosage Form', blank=True, default=list)
    route = models.JSONField(verbose_name='Route of Administration', blank=True, default=list)
    pharm_class = models.JSONField(verbose_name='Pharmacologic Class', blank=True, default=list)
    indications = models.TextField(blank=True, help_text="What conditions this drug is used to treat", verbose_name="Indications")
    side_effects = models.TextField(blank=True, verbose_name="Side Effects")
    precautions = models.TextField(blank=True, verbose_name="Precautions")
    active_ingredients = models.JSONField(verbose_name='Active Ingredients', blank=True, default=list)
    warnings = models.TextField(blank=True, verbose_name="Warnings")
    storage = models.CharField(max_length=2000, blank=True, help_text="e.g., Store below 25°C", verbose_name="Storage Instructions")
    manufacturer = models.CharField(max_length=200, blank=True, null=True, verbose_name="Manufacturer")
    is_prescription_required = models.BooleanField(default=True, verbose_name="Prescription Required?")
    img = models.ImageField(upload_to='images/drug_images/', blank=True, null=True, help_text="Uploaded image of the drug", storage=MediaCloudinaryStorage() if not settings.DEBUG else None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.name


class DrugStock(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='stocks', verbose_name="Drug")
    batch_number = models.CharField(max_length=100, verbose_name="Batch Number")
    name = models.CharField(max_length=100, verbose_name="Name", blank=True, null=True)
    strenght = models.CharField(max_length=100, verbose_name="Strenght", blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity in Stock")
    order_quantity = models.PositiveIntegerField(verbose_name="Quantity in Stock", default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Price")
    img = models.ImageField(upload_to='images/drug_images/', blank=True, null=True, help_text="Prescription Image", storage=MediaCloudinaryStorage() if not settings.DEBUG else None)
    expiry_date = models.DateField(verbose_name="Expiry Date")
    is_prescription_required = models.BooleanField(default=False, verbose_name="Prescription Required?")
    date_received = models.DateField(auto_now_add=True, verbose_name="Date Received")

    def __str__(self):
        return f"{self.drug.name} - Batch {self.batch_number}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ORDER_STATUS_CHOICES = [
        ('processing', 'Processing'),        
        ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='processing', verbose_name="Order Status")
    date = models.DateField(null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Order #{self.client}"
    
    def update_fields(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save(update_fields=['total_price'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    drug = models.ForeignKey(DrugStock, on_delete=models.SET_NULL, null=True, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prescription_image = models.ImageField(upload_to='images/orders/prescriptions/', blank=True, null=True, storage=MediaCloudinaryStorage() if not settings.DEBUG else None)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.drug.name} (x{self.quantity})" if self.drug else f"Item #{self.id}"
    
    def update_fields(self):
        drug_price = self.drug.price
        self.price = drug_price
        self.total_price = drug_price * Decimal(self.quantity)
        self.save(update_fields=['total_price', 'price'])


class Message(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(verbose_name='Sender Name', max_length=200, blank=True, null=True)
    message = models.TextField(verbose_name='Message', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.client} - {self.sender}"


class DietPlan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='diet_plans')
    goal = models.CharField(max_length=200, verbose_name="Diet Goal", blank=True, null=True)
    diet_type = models.CharField(max_length=100, choices=[("regular", "Regular"), ("vegetarian", "Vegetarian"), ("vegan", "Vegan"), ("keto", "Keto")])
    duration_days = models.IntegerField(default=7)
    meal_types = models.JSONField(verbose_name='Meal Types', blank=True, default=list, help_text="Describe your typical daily food intake (e.g., breakfast, lunch, dinner, snacks).")
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little to no exercise)'),
        ('lightly_active', 'Lightly Active (light exercise/sports 1-3 days/week)'),
        ('moderately_active', 'Moderately Active (moderate exercise/sports 3-5 days/week)'),
        ('very_active', 'Very Active (hard exercise/sports 6-7 days/week)'),
        ('extra_active', 'Extra Active (very hard exercise/physical job)'),
    ]
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, default='sedentary', help_text="Your daily activity level.")
    preferred_foods = models.JSONField(verbose_name='Preferred Foods', blank=True, default=list, help_text="List foods you particularly enjoy (e.g., fruits, vegetables, specific cuisines).")
    plans = models.JSONField(verbose_name='Plans', blank=True, default=list)
    end_date = models.DateField(null=True, blank=True, verbose_name='End Date')
    created_at = models.DateTimeField(auto_now_add=True)
