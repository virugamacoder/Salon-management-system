from datetime import datetime, time, timedelta
import datetime
import time
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from appointment.models import Service, Appointment
from myapp.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from myapp.models import OTP
import pyotp

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static
from django.utils.safestring import mark_safe

# Create your views here.


def step1(request):
    if request.user.is_authenticated and request.user.is_customer:
        service = Service.objects.all()
        SendService = request.POST.get("SendService", "")
        SendTime = request.POST.get("SendTime", "")
        SendDate = request.POST.get("SendDate", "")
        SendBarbar = request.POST.get("SendBarbar", "")

        data = {}
        data["SendService"] = SendService
        data["SendDate"] = SendDate
        data["SendTime"] = SendTime
        data["SendBarbar"] = SendBarbar
        data["service"] = service
        print("data step1 : ", data)
        return render(request, "appointment/step-1.html", data)
    else:
        messages.error(
            request, "Appintment Book Is Must User Login Required ! Please Login"
        )
        return redirect("loginpage")


@login_required(login_url="/")
def step2(request):
    if request.user.is_customer:
        if request.method == "POST":
            SendService = request.POST.get("SendService", "")
            SendTime = request.POST.get("SendTime", "")
            SendDate = request.POST.get("SendDate", "")
            SendBarbar = request.POST.get("SendBarbar", "")

            data = {}
            data["SendService"] = SendService
            data["SendDate"] = SendDate
            data["SendTime"] = SendTime
            data["SendBarbar"] = SendBarbar

            print("s : ", data["SendService"])

            start_date = datetime.date.today()
            #  start_date_str = '27-02-2023'
            #  start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y').date()

            end_date = start_date + datetime.timedelta(days=7)

            date = {}

            j = 1
            #    for n in range(int((end_date - start_date).days)):
            #      d= start_date + datetime.timedelta(n)
            #      date[f"{j}"] = {"date" : "",
            #                     "day" : "",
            #                     "mon" : ""}
            #      date[f"{j}"]['date'] = d.strftime("%d")
            #      date[f"{j}"]['day'] = d.strftime('%A')
            #      date[f"{j}"]['mon'] = d.strftime('%B')
            #      j=j+1

            for n in range(int((end_date - start_date).days)):
                d = start_date + datetime.timedelta(n)
                date[f"{j}"] = d
                j = j + 1

            dates = []

            while start_date <= end_date:
                dates.append(start_date)
                start_date += timedelta(days=1)

            if dates[0].month == dates[-1].month:
                month_range_str = dates[0].strftime("%B %Y")
            else:
                month_range_str = (
                    dates[0].strftime("%B") + "-" + dates[-1].strftime("%B %Y")
                )
            print(month_range_str)
            print(date)
            data["date"] = date
            data["month"] = month_range_str
            print("data step2 : ", data)
            return render(request, "appointment/step-2.html", data)
        else:
            return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="/")
def step3(request):
    if request.user.is_customer:
        if request.method == "POST":
            SendService = request.POST.get("SendService", "")
            SendTime = request.POST.get("SendTime", "")
            SendDate = request.POST.get("SendDate")
            SendBarbar = request.POST.get("SendBarbar", "")

            data = {}
            data["SendService"] = SendService
            data["SendDate"] = SendDate
            data["SendTime"] = SendTime
            data["SendBarbar"] = SendBarbar
            # date_obj = datetime.strptime(datetime_str, '%B %d, %Y')
            print("data step3 : ", data)
            barbar = User.objects.filter(is_employee=True)
            data["barbar"] = barbar

            print("data step3 : ", data)
            return render(request, "appointment/step-3.html", data)
        else:
            return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="/")
def step4(request):
    if request.user.is_customer:
        if request.method == "POST":
            SendTime = request.POST.get("SendTime", "")
            SendDate = request.POST.get("SendDate", "")
            SendService = request.POST.get("SendService", "")
            SendBarbar = request.POST.get("SendBarbar")
            data = {}
            data["SendBarbar"] = SendBarbar
            data["SendService"] = SendService
            data["SendDate"] = SendDate
            data["SendTime"] = SendTime

            Barbar = User.objects.filter(id=SendBarbar)
            ServiceArray = SendService.split(",")
            print(ServiceArray)

            appointment_total = 0
            for sid in ServiceArray:
                s, created = Service.objects.get_or_create(sid=sid)
                appointment_total = appointment_total + s.sprice

            service_id = Service.objects.filter(sid__in=ServiceArray)
            data["Service"] = service_id
            data["Barbar"] = Barbar
            data["total"] = appointment_total

            return render(request, "appointment/step-4.html", data)
        else:
            return redirect("home")
    else:
        return redirect("home")


def generate_otp(email):
    totp = pyotp.TOTP("base32secret3232")
    otp_value = totp.now()
    send_otp_email(email, otp_value)
    print("otp = ", otp_value)
    return otp_value


def sendemail(subject, message, email):
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_otp_email(email, otp_value):
    subject = "Appointment OTP Verification"
    message = f"<br> Your OTP is {otp_value}."
    message = mark_safe(message)
    send_email(email, subject, message)


@login_required(login_url="/")
def book(request):
    if request.user.is_customer:
        if request.method == "POST":
            SendTime = request.POST.get("SendTime", "")
            SendDate = request.POST.get("SendDate", "")
            SendService = request.POST.get("SendService", "")
            SendBarbar = request.POST.get("SendBarbar", "")
            SendMno = request.POST.get("SendMno", "")
            email = request.user.email
            otp = generate_otp(email)

            request.session["appointment"] = {
                "SendDate": SendDate,
                "SendTime": SendTime,
                "SendService": SendService,
                "SendBarbar": SendBarbar,
                "SendMno": SendMno,
                "otp": otp,
            }
            return redirect("/a/otppage/")

        else:
            return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="/")
def otpvalidate(request):
    if request.user.is_customer:
        if request.method == "POST":
            i1 = request.POST.get("otpi1", "")
            i2 = request.POST.get("otpi2", "")
            i3 = request.POST.get("otpi3", "")
            i4 = request.POST.get("otpi4", "")
            i5 = request.POST.get("otpi5", "")
            i6 = request.POST.get("otpi6", "")

            reciveotp = i1 + i2 + i3 + i4 + i5 + i6
            otp = request.session["appointment"]["otp"]
            if reciveotp == otp:
                messages.success(
                    request, "Otp Validate Successfully Appointment Booking"
                )

                return redirect("/a/finalbook/")
            else:
                messages.success(request, "You Enter Otp Is Incorrect !")
                return redirect("/a/otppage/")
    else:
        return redirect("home")


@login_required(login_url="/")
def finalbook(request):
    if request.user.is_customer:
        SendDate = request.session["appointment"]["SendDate"]
        SendTime = request.session["appointment"]["SendTime"]
        SendService = request.session["appointment"]["SendService"]
        SendBarbar = request.session["appointment"]["SendBarbar"]
        SendMno = request.session["appointment"]["SendMno"]

        try:
            ServiceArray = SendService.split(",")
            data = {}
            appointment_date = datetime.datetime.strptime(SendDate, "%B %d, %Y")
            start_time, end_time = SendTime.split(" - ")
            start_time = datetime.datetime.strptime(start_time, "%H:%M")
            end_time = datetime.datetime.strptime(end_time, "%H:%M")
            emp_id = User.objects.filter(id=SendBarbar)
            emp_id = emp_id.first()
            print("emp_id = ", emp_id)
            slist = []
            appointment_total = 0
            service_str = ""
            for sid in ServiceArray:
                s, created = Service.objects.get_or_create(sid=sid)
                slist.append(s)
                service_str = service_str + " " + s.sname
                appointment_total = appointment_total + s.sprice

            duration = end_time - start_time

            final_appointment = Appointment.objects.create(
                cid=request.user,
                adate=appointment_date,
                atime=start_time,
                eid=emp_id,
                aduration=duration,
                aprice=appointment_total,
                astatus="SCHEDULED",
                mobile_no=SendMno,
            )

            final_appointment.sid.set(slist)

            subject = "Appointment Of BarberShop Services"
            appointment_msg = f"<br> * Your Appointment Is Date = {SendDate}"
            atime_msg = f"<br> * Your Appointment Is Time = {SendTime}"
            service_msg = f"<br> * Service = {service_str}"
            total_msg = f"<br> * Total Pay Rupees = {appointment_total}"
            message = appointment_msg + service_msg + total_msg
            message = mark_safe(message)
            email = request.user.email
            send_email(email, subject, message)
            del request.session["appointment"]
            return redirect("/a/finish/")
        except Exception as e:
            messages.error(request, e)
            return redirect("home")

    else:
        return redirect("home")


@login_required(login_url="/")
def otppage(request):
    if request.user.is_customer:
        return render(request, "appointment/otppage.html")


@login_required(login_url="/")
def finish(request):
    if request.user.is_customer:
        return render(request, "appointment/finish.html")


def send_email(email, subject, message):
    logo_url = static("images/logo-default-dark-200x36.png")

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    html_message = render_to_string(
        "email_templates/email.html",
        {"subject": subject, "message": message, "logo_url": logo_url},
    )
    mail = EmailMultiAlternatives(subject, "", from_email, recipient_list)
    mail.attach_alternative(html_message, "text/html")
    mail.send()
