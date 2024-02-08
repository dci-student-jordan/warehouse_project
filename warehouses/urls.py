from django.urls import path, include
from .views import (
    Index,
    Warehouse,
    About,
    Products,
    RegisterView,
    LoginView,
    SignUpView,
    UpdateUserView,
    ContactView
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("about", About.as_view(), name="about"),
    path("<str:location>", Warehouse.as_view(), name="warehouse"),
    path("<str:location>/products", Products.as_view(), name="products"),
    path("user/login", LoginView.as_view(), name="login"),
    path("user/signup", SignUpView.as_view(), name="signup"),
    path("user/contact", ContactView.as_view(), name="contact"),
    path("user/register", RegisterView.as_view(), name="register"),
    path("user/account/<int:pk>", UpdateUserView.as_view(), name="account"),
    path('user/', include('django.contrib.auth.urls')),
]