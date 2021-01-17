from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name="register"),
    path('user/<str:pk>', profile_view, name="profile"),
    path('user/edit-profile/', edit_profile_view, name="edit-profile"),
    path('user/settings/', settings_view, name="settings"),
    path('donors/', donor_view, name="donors"),
    path('contact/', contact_view, name="contact"),
    path('notifications/', notification_view, name="notification"),

    path('reset-password/',
         auth_views.PasswordResetView.as_view(template_name="password-reset.html"),
         name="reset-password"),
    path('reset-password-sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password-reset-sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-form.html"),
         name="password_reset_confirm"),

    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-done.html"),
         name="password_reset_complete"),
]
