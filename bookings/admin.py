from django.contrib import admin
from .models import Apartment, ApartmentImage


class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 1  # how many rows to show

class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInline]

admin.site.register(Apartment, ApartmentAdmin)
