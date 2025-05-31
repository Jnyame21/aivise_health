from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(Staff)
admin.site.register(Client)
admin.site.register(Consultation)
admin.site.register(StaffImageFile)
admin.site.register(ClientImageFile)
admin.site.register(Drug)
admin.site.register(Message)
admin.site.register(DietPlan)
admin.site.register(DrugStock)