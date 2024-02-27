# user.urls.py

from django.urls import path, include
from warehouses.views import RegisterView
from .views import (
    LoginView,
    SignUpView,
    UpdateUserView,
    ContactView,
    custom_logout,
    LoginRequiredView,
    ConnectEmployeeView
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login_to_cli_account/", ConnectEmployeeView.as_view(), name="connect_employee"),
    path("account/<int:pk>", UpdateUserView.as_view(), name="account"),
    path('auth/', include('django.contrib.auth.urls')),
    path('logout/', custom_logout, name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("login_required/", LoginRequiredView.as_view(), name="login_required"),
]