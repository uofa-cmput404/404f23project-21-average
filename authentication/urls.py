from authentication.views import RegistrationView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path
from rest_framework.authtoken import views as authviews


urlpatterns = [
    path("register/", RegistrationView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path('token/', authviews.obtain_auth_token, name="api-token-auth"),
]
