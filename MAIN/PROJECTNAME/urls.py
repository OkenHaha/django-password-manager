
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("APPNAME.urls")),

    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    # path('reset/<uid64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    # path('reset_password_success/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_sent.html"), name="password_reset_complete"),

]