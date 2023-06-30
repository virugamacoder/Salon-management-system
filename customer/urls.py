from django.urls import path
from.import views
urlpatterns = [
     path('', views.cdashboard, name="cdashboard"),
     path('aview/',views.aview,name="aview"),
    path('adelete/<int:aid>/', views.adelete, name="adelete"),
    path('profile/', views.profile, name="profile"),
    path('editprofile/', views.editprofile, name="editprofile"),
    path('orderhistory/', views.orderhistory, name="orderhistory"),
    path('vieworder/<int:oid>/', views.vieworder, name="vieworder"),
    path('deleteorder/<int:oid>/', views.deleteorder, name="deleteorder"),


]