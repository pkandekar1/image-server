from django.contrib import admin
from .models import MenuItem
# Register your models here.
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'restaurant_name')
    search_fields = ('name', 'restaurant_name')
admin.site.register(MenuItem,MenuItemAdmin)