from django.contrib import admin
from .models import User,UserProfile

# Register your models here.
@admin.register(User)
class OrderplacedAdminModel(admin.ModelAdmin):
    list_display = ['id', 'email', 'last_name',]
admin.site.register(UserProfile)