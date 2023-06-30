from django.urls import path
from . import views

urlpatterns = [
    path("", views.edashboard, name="edashboard"),
    path("aview/", views.aview, name="aview"),
    path("eprofile/", views.eprofile, name="eprofile"),
    path("editprofile/", views.editprofile, name="editprofile"),
    path("manageleave/", views.manageleave, name="manageleave"),
    path("getleave/", views.getleave, name="getleave"),
    path("cancelleave/<int:lid>/", views.cancelleave, name="cancelleave"),
    path("astatus/<int:aid>/", views.astatus, name="astatus"),
]
