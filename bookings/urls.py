from django.urls import path
from .views import auth_views, apartment_views


app_name = 'bookings'

urlpatterns = [
    path('', auth_views.home, name='home'),
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login_request, name='login'),
    path('apartments/', apartment_views.apartments_view, name='apartments'),
    path('apartments/<int:apartment_id>/', apartment_views.apartment_detail, name='apartment_detail'),

]