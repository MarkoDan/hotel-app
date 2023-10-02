from django.contrib import admin
from .models import Apartment, ApartmentImage, Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'user', 'user_full_name_display')
    
    def user_full_name_display(self, obj):
        return obj.user_full_name
    user_full_name_display.short_description = 'User Full Name'


class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 1  # how many rows to show

class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInline]

admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Booking, BookingAdmin)
