from django.urls import path
from django.contrib.auth import views as auth_views
from . import auth_views


app_name = 'bookings'

urlpatterns = [
    path('', auth_views.home, name='home'),
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login_request, name='login'),

]