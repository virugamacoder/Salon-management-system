from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.text import Truncator
from shop.models import Order, OrderItem
from appointment.models import *
from myapp.models import *
from django.contrib import messages
import os
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/")
def cdashboard(request):
    if request.user.is_authenticated and request.user.is_customer:
        return render(request, "customer/cdashboard.html")
    else:
        return redirect("home")


@login_required(login_url="/")
def aview(request):
    if request.user.is_authenticated and request.user.is_customer:
        #  appointment=Appointment.objects.filter(cid=request.user)
        #  data={'appointment':appointment}
        today = timezone.now().date()
        past = Appointment.objects.filter(adate__lt=today, cid=request.user).order_by(
            "adate", "atime"
        )
        present = Appointment.objects.filter(adate=today, cid=request.user).order_by(
            "atime"
        )
        future = Appointment.objects.filter(adate__gt=today, cid=request.user).order_by(
            "adate", "atime"
        )
        # print(appointment)
        data = {"past": past, "present": present, "future": future}
        return render(request, "customer/aview.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def adelete(request, aid):
    if request.user.is_authenticated and request.user.is_customer:
        appointment = Appointment.objects.get(aid=aid, cid=request.user)
        appointment.delete()
        messages.success(request, "Your appointment is succesfully Cancel ")

        return redirect("/customer/aview/")
    else:
        return redirect("home")


@login_required(login_url="/")
def profile(request):
    if request.user.is_authenticated and request.user.is_customer:
        uid = request.user
        user = User.objects.get(id=request.user.id)

        return render(request, "customer/profile.html", {"user": user})
    else:
        return redirect("home")


@login_required(login_url="/")
def editprofile(request):
    if request.user.is_authenticated and request.user.is_customer:
        user = User.objects.get(id=request.user.id)

        if request.method == "POST":
            # id = request.POST.get('id')
            if len(request.FILES) != 0:
                if user.uimg:
                    if "uimg" in request.FILES:
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(user.uimg)))

                uimg = request.FILES["uimg"]
                user.uimg = uimg

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            gender = request.POST.get("gender")
            # email = request.POST.get('email')
            phone = request.POST.get("phone")

            user.first_name = first_name
            user.last_name = last_name
            user.gender = gender
            user.phone = phone
            print(gender)
            user.save()
            messages.success(request, "Your Profile is succesfully Updated ")

            return redirect("profile")

        return render(request, "customer/editprofile.html", {"user": user})
    else:
        return redirect("home")


# order
@login_required(login_url="/")
def orderhistory(request):
    if request.user.is_authenticated and request.user.is_customer:
        # orderitem =OrderItem.objects.all()
        dorder = Order.objects.filter(delivered_status="YES", cid=request.user).order_by('-oid')
        order = Order.objects.filter(delivered_status="NO", cid=request.user).order_by('-oid')
        data = {"order": order, "dorder": dorder}
        # if request.method=='POST':

        return render(request, "customer/orderhistory.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def vieworder(request, oid):
    if request.user.is_authenticated and request.user.is_customer:
        order = Order.objects.get(oid=oid, cid=request.user)
        orderitem = OrderItem.objects.filter(oid=oid)
        data = {"orderitem": orderitem, "order": order}

        return render(request, "customer/vieworder.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def deleteorder(request, oid):
    if request.user.is_authenticated and request.user.is_customer:
        order = Order.objects.get(oid=oid, cid=request.user)
        #  appointment = Appointment.objects.get(aid=aid, cid=request.user)
        order.delete()
        messages.success(request, "Your Order is succesfully Cancel ")

        return redirect("orderhistory")
    # return render(request,'customer/aview.html',data)
    else:
        return redirect("home")
