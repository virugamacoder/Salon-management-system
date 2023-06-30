from django.urls import path
from . import views

urlpatterns = [
    # path('', views.main, name="main"),
    # path('', views.admin_login, name="admin_login"),
    # path('main/', views.main, name="main"),
    path("", views.dashboard, name="dashboard"),
    #  product
    path("product/manageprod/", views.manageprod, name="manageprod"),
    path("product/add/", views.add, name="add"),
    path("product/update/<int:pid>/", views.update, name="update"),
    path("product/delete/<int:pid>/", views.delete, name="delete"),
    path("product/stock/<int:pid>/", views.stock, name="stock"),
    # service
    path("service/manageservice/", views.manageservice, name="manageservice"),
    path("service/sadd/", views.sadd, name="sadd"),
    path("service/sdelete/<int:sid>/", views.sdelete, name="sdelete"),
    # path('service/sedit/<int:sid>/', views.sedit, name="sedit"),
    path("service/supdate/<int:sid>/", views.supdate, name="supdate"),
    # employee
    path("emp/manageemp/", views.manageemp, name="manageemp"),
    path("emp/empadd/", views.empadd, name="empadd"),
    path("emp/empupdate/<int:id>/", views.empupdate, name="empupdate"),
    path("emp/empdelete/<int:id>/", views.empdelete, name="empdelete"),
    # customer
    path("customer/managecustomer/", views.managecustomer, name="managecustomer"),
    path("customer/custadd/", views.custadd, name="custadd"),
    path("customer/custdelete/<int:id>/", views.custdelete, name="custdelete"),
    # appoint ment
    path(
        "appointment/manageappointment/",
        views.manageappointment,
        name="manageappointment",
    ),
    path("appointment/astatus/<int:aid>/", views.astatus, name="astatus"),
    # manage order
    path("order/manageorder/", views.manageorder, name="manageorder"),
    path("order/vieworder/<int:oid>/", views.vieworder, name="vieworder"),
    # path('order/editorder/<int:oid>/', views.editorder, name="editorder"),
    # profile
    path("adminprofile/", views.adminprofile, name="adminprofile"),
    path("admineditprofile/", views.admineditprofile, name="admineditprofile"),
    # leave
    path("leave/manageleave/", views.manageleave, name="manageleave"),
    path("leave/editleave/<int:lid>/", views.editleave, name="editleave"),
]
