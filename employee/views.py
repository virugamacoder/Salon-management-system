from django.shortcuts import render
from datetime import datetime, time, timedelta

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.text import Truncator
from shop.models import Product, Order, OrderItem
from appointment.models import Appointment, Service
from myapp.models import User
from employee.models import Leave
from django.db.models import Q

from django.contrib import messages
import os
from django.utils import timezone

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/")
def edashboard(request):
    if request.user.is_authenticated and request.user.is_employee:
        return render(request, "employee/edashboard.html")
    else:
        return redirect("home")


@login_required(login_url="/")
def aview(request):
    if request.user.is_authenticated and request.user.is_employee:
        today = timezone.now().date()
        print(today)
        past = Appointment.objects.filter(adate__lt=today, eid=request.user).order_by(
            "adate", "atime"
        )
        present = Appointment.objects.filter(adate=today, eid=request.user).order_by(
            "atime"
        )
        future = Appointment.objects.filter(adate__gt=today, eid=request.user).order_by(
            "adate", "atime"
        )

        data = {"past": past, "present": present, "future": future}
        print(data)

        return render(request, "employee/aview.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def eprofile(request):
    if request.user.is_authenticated and request.user.is_employee:
        user = User.objects.get(id=request.user.id)
        return render(request, "employee/eprofile.html", {"user": user})
    else:
        return redirect("home")


def editprofile(request):
    if request.user.is_authenticated and request.user.is_employee:
        user = User.objects.get(id=request.user.id)

        if request.method == "POST":
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
            messages.success(request, "Your Employee is succesfully Updated ")
            return redirect("eprofile")

        return render(request, "employee/editprofile.html", {"user": user})
    else:
        return redirect("home")


@login_required(login_url="/")
def manageleave(request):
    if request.user.is_authenticated and request.user.is_employee:
        #    leavecreate=
        leave = Leave.objects.filter(
            Q(lstatus="APPROVAL") | Q(lstatus="NOTAPPROVAL"), eid=request.user
        )
        leavepending = Leave.objects.filter(Q(lstatus="PENDING"), eid=request.user)

        data = {"leave": leave, "leavepending": leavepending}
        return render(request, "employee/manageleave.html", data)

    else:
        return redirect("home")


@login_required(login_url="/")
def getleave(request):
    if request.user.is_authenticated and request.user.is_employee:
        if request.method == "POST":
            lreson = request.POST.get("lreson")
            lstart_date = request.POST.get("lstart_date")
            lend_date = request.POST.get("lend_date")
            start = datetime.strptime(lstart_date, "%Y-%m-%d")
            end = datetime.strptime(lend_date, "%Y-%m-%d")

            leave = Leave(
                eid=request.user,
                lreson=lreson,
                lstart_date=lstart_date,
                lend_date=lend_date,
                ldays=(end - start).days,
            )

            leave.save()
            messages.success(
                request, "Your Employee is succesfully Leave Request Send "
            )
            return redirect("manageleave")

        return render(request, "employee/getleave.html")

    else:
        return redirect("home")


@login_required(login_url="/")
def cancelleave(request, lid):
    if request.user.is_authenticated and request.user.is_employee:
        leave = Leave.objects.get(lid=lid, eid=request.user)
        leave.delete()
        messages.success(request, "Your Leave is succesfully Cancel ")

        return redirect("manageleave")
    # return render(request,'customer/aview.html',data)
    else:
        return redirect("home")


@login_required(login_url="/")
def astatus(request, aid):
    if request.user.is_authenticated and request.user.is_employee:
        appointment = Appointment.objects.get(aid=aid)

        if request.method == "POST":
            pmethod = request.POST.get("pmethod")

            if pmethod == "CASH":
                Appointment.objects.filter(aid=aid, eid=request.user).update(
                    astatus="COMPLETED"
                )
                messages.success(
                    request, "Appointment Service And Payment Succesfully Complted"
                )
                return redirect("/employee/aview/")
            elif pmethod == "ONLINE":
                return redirect("/employee/aview/")
        return render(
            request, "employee/manageastatus.html", {"appointment": appointment}
        )
    else:
        return redirect("home")


# manageastatus.html
