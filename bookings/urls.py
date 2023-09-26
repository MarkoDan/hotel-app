from django.urls import path
from .views import auth_views, apartment_views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import views as authentication_views
from django.urls import reverse_lazy



app_name = 'bookings'

urlpatterns = [
    path('', auth_views.home, name='home'),
    path('register/', auth_views.register, name='register'),
    path('login/', LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', auth_views.logout_request, name='logout'),
    path('apartments/', apartment_views.apartments_view, name='apartments'),
    path('apartments/<int:apartment_id>/', apartment_views.apartment_detail, name='apartment_detail'),
    path('contact/', auth_views.contact, name='contact'),


    #Profile urls
    path('profile/', auth_views.profile_view, name='profile'),
    path('profile/delete', auth_views.delete_account, name='delete_account'),
    path('password_change/', PasswordChangeView.as_view(template_name='bookings/password_change.html',success_url=reverse_lazy('bookings:password_change_done')), name='password_change'),


    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='bookings/password_change_done.html'), name='password_change_done'),
    #Password reset links
    path('password-reset/', authentication_views.PasswordResetView.as_view(template_name='bookings/registration/password_reset.html',success_url=reverse_lazy('bookings:password_reset_done')), name='password_reset'),
    path('password-reset/done/', authentication_views.PasswordResetDoneView.as_view(template_name='bookings/registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', authentication_views.PasswordResetConfirmView.as_view(template_name='bookings/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', authentication_views.PasswordResetCompleteView.as_view(template_name='bookings/registration/password_reset_complete.html'), name='password_reset_complete'),

]