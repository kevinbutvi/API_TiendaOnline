from . import views
from django.urls import path, include

urlpatterns = [
    path(
        'login/',
        views.LoginUser.as_view(),
        name="login"
        ),
    path(
        'api/google-login/',
        views.GoogleLoginView.as_view(),
        name="users-google_login"
        ),
]