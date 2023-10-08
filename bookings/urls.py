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
    path('privacy-policy/', auth_views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', auth_views.terms_and_conditions, name='terms_and_conditions'),
    
    path('apartment/', apartment_views.book_apartment, name='book_apartment'),
    path('booking-success/', apartment_views.booking_success, name='booking_success'),
    path('booking-failed/', apartment_views.booking_failed, name='booking_failed'),

    #availability

    path('check_availability/', apartment_views.check_availability, name='check_availability'),
    path('availability_result/<str:available>/', apartment_views.availability_result, name='availability_result'),

    #Profile urls
    path('profile/', auth_views.profile_view, name='profile'),
    path('profile/delete', auth_views.delete_account, name='delete_account'),
    path('password_change/', PasswordChangeView.as_view(template_name='bookings/password_change.html',success_url=reverse_lazy('bookings:password_change_done')), name='password_change'),


    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    #Password reset links
    path('password-reset/', authentication_views.PasswordResetView.as_view(template_name='registration/password_reset.html',success_url=reverse_lazy('bookings:password_reset_done')), name='password_reset'),
    path('password-reset/done/', authentication_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', authentication_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', authentication_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    #payment urls
    path('start-payment/', apartment_views.start_payment, name='start_payment'),
    path('stripe/webhook/', apartment_views.StripeWebhook.as_view(), name='stripe_webhook'),

    #canceling booking urls
    path('booking/cancel/<int:booking_id>/', apartment_views.cancel_booking, name='cancel_booking'),

    #Bookings
    path('display-bookings/', apartment_views.display_bookings, name='display_bookings'),
]