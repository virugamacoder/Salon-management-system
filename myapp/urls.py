from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("barbers/", views.barbers, name="barbers"),
    path("services/", views.services, name="services"),
    path("login/", views.loginpage, name="loginpage"),
    path("loginhandle/", views.loginhandle, name="loginhandle"),
    path("signup/", views.signup, name="signup"),
    path("signuphandle/", views.signuphandle, name="signuphandle"),
    path("otppage/", views.otppage, name="otppage"),
    path("otppage2/", views.otppage2, name="otppage2"),
    path("otpvalidate/", views.otpvalidate, name="otpvalidate"),
    path("resetpassvalidate/", views.resetpassvalidate, name="resetpassvalidate"),
    path("resetpass1/", views.resetpass1, name="resetpass1"),
    path("resetpass2/", views.resetpass2, name="resetpass2"),
    path("logout/", views.logoutpage, name="logoutpage"),
]
