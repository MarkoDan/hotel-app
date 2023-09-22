from django.urls import path
from .views import auth_views, apartment_views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView


app_name = 'bookings'

urlpatterns = [
    path('', auth_views.home, name='home'),
    path('register/', auth_views.register, name='register'),
    path('login/', LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', auth_views.logout_request, name='logout'),
    path('apartments/', apartment_views.apartments_view, name='apartments'),
    path('apartments/<int:apartment_id>/', apartment_views.apartment_detail, name='apartment_detail'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('password_change/', PasswordChangeView.as_view(template_name='bookings/password_change.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='bookings/password_change_done.html'), name='password_change_done'),

]