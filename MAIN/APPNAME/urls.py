from django.urls import path
from .views import home
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("", home, name="home"),
    path('register/', views.registerPage, name="register"),

    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),
]