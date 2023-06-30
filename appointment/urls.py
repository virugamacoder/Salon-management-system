from django.urls import path
from . import views

urlpatterns = [
    path("step1/", views.step1, name="step1"),
    path("step2/", views.step2, name="step2"),
    path("step3/", views.step3, name="step3"),
    path("step4/", views.step4, name="step4"),
    path("book/", views.book, name="book"),
    path("finalbook/", views.finalbook, name="finalbook"),
    path("otppage/", views.otppage, name="otppage"),
    path("otpvalidate/", views.otpvalidate, name="otpvalidate"),
    path("finish/", views.finish, name="finish"),
]
