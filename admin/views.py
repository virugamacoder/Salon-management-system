from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from shop.models import *
from shop.models import Product, Order, OrderItem
from appointment.models import *
from employee.models import *
from django.utils.safestring import mark_safe
from myapp.models import User
import os
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db.models import Case, When
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static


# from .forms import ImageUploadForm
# from pillow import Image
# Create your views here.


@login_required(login_url="/")
def dashboard(request):
    if request.user.is_authenticated and request.user.is_admin:
        today = timezone.now().date()

        present = Appointment.objects.filter(adate=today).count()
        future = Appointment.objects.filter(adate__gt=today).count()

        # order

        order = Order.objects.filter(delivered_status="NO").count()
        # leave
        pendingleave = Leave.objects.filter(Q(lstatus="PENDING")).count()

        # service & product
        totalservice = Service.objects.count()
        totalproduct = Product.objects.count()

        customer = User.objects.filter(is_customer=True).count()
        employee = User.objects.filter(is_employee=True).count()

        context = {
            "customer": customer,
            "present": present,
            "future": future,
            "order": order,
            "pendingleave": pendingleave,
            "totalservice": totalservice,
            "totalproduct": totalproduct,
            "employee": employee,
        }
        return render(request, "admin/dashboard.html", context)
    else:
        return redirect("home")


#  Product Manage
@login_required(login_url="/")
def manageprod(request):
    if request.user.is_authenticated and request.user.is_admin:
        products = Product.objects.all().order_by("-pid")
        print(products)
        data = {"products": products}
        return render(request, "admin/product/manageprod.html", data)
    else:
        return redirect("home")


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


@login_required(login_url="/")
def add(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == "POST":
            pname = request.POST.get("pname", "")
            pprice = int(request.POST.get("pprice", ""))
            pdesc = request.POST.get("pdesc", "")
            pinfo = request.POST.get("pinfo", "")
            pstock = int(request.POST.get("pstock", ""))
            pimg = request.FILES["pimg"]

            product = Product(
                pname=pname,
                pprice=pprice,
                pdesc=pdesc,
                pinfo=pinfo,
                pstock=pstock,
                pimg=pimg,
            )
            product.save()
            messages.success(request, "Your product is succesfully Added  ")
            return redirect("manageprod")

        return render(request, "admin/product/add.html")
    else:
        return redirect("home")


@login_required(login_url="/")
def update(request, pid):
    if request.user.is_authenticated and request.user.is_admin:
        product = Product.objects.get(pid=pid)

        if request.method == "POST":
            if len(request.FILES) != 0:
                if len(product.pimg) > 0:
                    os.remove(product.pimg.path)
                pimg = request.FILES["pimg"]
                product.pimg = pimg
            pid = request.POST.get("pid")
            pname = request.POST.get("pname")
            pprice = int(request.POST.get("pprice"))
            pdesc = request.POST.get("pdesc")
            pinfo = request.POST.get("pinfo")

            # pimg = request.FILES['pimg']

            product.pname = pname
            product.pprice = pprice
            product.pdesc = pdesc
            product.pinfo = pinfo
            # product.pimg=pimg
            print(pname)
            print(pprice)
            product.save()
            messages.success(request, "Your product is succesfully Updated ")
            return redirect("manageprod")

        return render(request, "admin/product/update.html", {"product": product})
    else:
        return redirect("home")


# stock


@login_required(login_url="/")
def stock(request, pid):
    if request.user.is_authenticated and request.user.is_admin:
        product = Product.objects.get(pid=pid)
        print(product)
        data = {"product": product}
        if request.method == "POST":
            pstock = request.POST.get("pstock")
            product.pstock = pstock
            product.save()
            return redirect("manageprod")
        return render(request, "admin/product/stock.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def delete(request, pid):
    if request.user.is_authenticated and request.user.is_admin:
        product = Product.objects.get(pid=pid)
        product.delete()
        data = {"products": product}
        print(data)
        messages.success(request, "Your product is succesfully Deleted ")
        return redirect("manageprod")
    else:
        return redirect("home")


@login_required(login_url="/")
def manageservice(request):
    if request.user.is_authenticated and request.user.is_admin:
        service = Service.objects.all().order_by("-sid")
        print(service)
        data = {"service": service}
        return render(request, "admin/service/manageservice.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def sadd(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == "POST":
            sname = request.POST.get("sname", "")
            sprice = request.POST.get("sprice", "")
            sdesc = request.POST.get("sdesc", "")
            simg = request.FILES["simg"]
            # service = Service(sname=sname, sprice=sprice, sdesc=sdesc,simg=simg)
            # if (sname!=None):
            #      messages.success(request, "Please Enter valid data  ")
            #      return redirect("sadd")
            # else:
            service = Service(sname=sname, sprice=sprice, sdesc=sdesc, simg=simg)
            service.save()
            messages.success(request, "Your Service is succesfully Added  ")
            return redirect("manageservice")

        return render(request, "admin/service/sadd.html")
    else:
        return redirect("home")


@login_required(login_url="/")
def sdelete(request, sid):
    if request.user.is_authenticated and request.user.is_admin:
        service = Service.objects.get(sid=sid)
        service.delete()
        data = {"Service": service}
        messages.success(request, "Your Service is succesfully Deleted ")
        print(data)
        return redirect("manageservice")
    else:
        return redirect("home")


@login_required(login_url="/")
def supdate(request, sid):
    if request.user.is_authenticated and request.user.is_admin:
        service = Service.objects.get(sid=sid)

        if request.method == "POST":
            if len(request.FILES) != 0:
                if len(service.simg) > 0:
                    os.remove(service.simg.path)
                simg = request.FILES["simg"]
                service.simg = simg
            sid = request.POST.get("sid")
            sname = request.POST.get("sname")
            sprice = int(request.POST.get("sprice"))
            sdesc = request.POST.get("sdesc")
            service.sname = sname
            service.sprice = sprice
            service.sdesc = sdesc
            # service.simg = simg
            print(sname)
            print(sprice)
            # service = Service( sid=sid, sname=sname, sprice=sprice, sdesc=sdesc,simg=simg)
            service.save()
            messages.success(request, "Your product is succesfully Updated ")
            return redirect("manageservice")

        return render(request, "admin/service/supdate.html", {"service": service})
    else:
        return redirect("home")


# manage employee
@login_required(login_url="/")
def manageemp(request):
    if request.user.is_authenticated and request.user.is_admin:
        emp = User.objects.filter(is_employee=True).order_by("-id")
        # emp= Employee.objects.all()
        print(emp)
        data = {"emp": emp}
        return render(request, "admin/emp/manageemp.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def empadd(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            gender = request.POST.get("gender")
            phone = request.POST.get("phone")
            skill = request.POST.get("skill")
            info = request.POST.get("info")

            uimg = request.FILES["uimg"]

            try:
                emp = User.objects._create_user(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    email=email,
                    password=password,
                    phone=phone,
                    uimg=uimg,
                    is_employee=True,
                )
                emp.save()
                e = User_Employee.objects.create(
                    emp=emp, infromation=info, skills=skill
                )
                subject = "BarbaerShop You Are New Barbers"
                message = "Login Email ID And PassWord Sent "
                message = message + "\n <br> Login Email ID = " + email
                message = message + "\n <br> Login Password = " + password
                message = mark_safe(message)
                send_email(email, subject, message)
                print("e ", emp, " e1 = ", e)
                messages.success(request, "Your Employee is succesfully Added  ")
            except Exception as e:
                messages.error(request, e)
                return redirect("/admin/emp/empadd/")

            return redirect("manageemp")

        return render(request, "admin/emp/empadd.html")
    else:
        return redirect("home")


@login_required(login_url="/")
def empupdate(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        emp1 = User.objects.get(id=id)
        emp = User_Employee.objects.get(emp=emp1)
        print(emp.emp.id)

        if request.method == "POST":
            if len(request.FILES) != 0:
                # if emp1.uimg:
                #     if "uimg" in request.FILES:
                #         os.remove(os.path.join(settings.MEDIA_ROOT, str(emp1.uimg)))
                # uimg = request.FILES["uimg"]
                # emp1.uimg = uimg

                if len(request.FILES) != 0:
                    if len(emp1.uimg) > 0:
                        os.remove(emp1.uimg.path)
                    uimg = request.FILES["uimg"]
                    emp1.uimg = uimg

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            gender = request.POST.get("gender")
            phone = request.POST.get("phone")
            skill = request.POST.get("skill")
            info = request.POST.get("info")
            # join_dated = request.POST.get('join_dated')

            emp1.first_name = first_name
            emp1.last_name = last_name
            emp1.gender = gender
            emp1.phone = phone
            emp.infromation = info
            emp.skills = skill
            emp1.save()
            emp.save()
            messages.success(request, "Your Employee is succesfully Updated ")
            return redirect("manageemp")

        return render(request, "admin/emp/empupdate.html", {"emp": emp})
    else:
        return redirect("home")


@login_required(login_url="/")
def empdelete(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        emp = User.objects.get(id=id)
        emp.delete()
        print(emp)
        messages.success(request, "Your Employee is succesfully deleted ")
        return redirect("manageemp")
    else:
        return redirect("home")

    # return render(request, 'admin/emp/empadd.html',{'emp':emp})


@login_required(login_url="/")
def managecustomer(request):
    if request.user.is_authenticated and request.user.is_admin:
        customer = User.objects.filter(is_customer=True).order_by("-id")
        # emp= Employee.objects.all()
        print(customer)
        data = {"customer": customer}
        return render(request, "admin/customer/managecustomer.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def custadd(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == "POST":
            try:
                email = request.POST.get("email")
                password = request.POST.get("password")
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                gender = request.POST.get("gender")
                phone = request.POST.get("phone")
                # uimg = request.FILES['uimg']
                customer = User.objects._create_user(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    email=email,
                    password=password,
                    phone=phone,
                    # uimg=uimg,
                    is_customer=True,
                )
                customer.save()
                subject = "BarbaerShop You Are New Customers"
                message = "Login Email ID And PassWord Sent "
                message = message + "\n<br>Login Email ID = " + email
                message = message + "\n<br>Login Password = " + password
                message = mark_safe(message)
                send_email(email, subject, message)

                print(customer)
                messages.success(request, "Your customer is succesfully Added  ")
                return redirect("managecustomer")
            except Exception as e:
                messages.error(request, e)

        return render(request, "admin/customer/custadd.html")
    else:
        return redirect("home")


@login_required(login_url="/")
def custdelete(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        customer = User.objects.get(id=id)
        customer.delete()
        print(customer)
        messages.success(request, "Your Customeris is succesfully deleted ")
        return redirect("managecustomer")
    else:
        return redirect("home")


#  appointment
@login_required(login_url="/")
def manageappointment(request):
    if request.user.is_authenticated and request.user.is_admin:
        # appointment = Appointment.objects.all()
        today = timezone.now().date()
        Appointment.objects.filter(adate__lt=today, astatus="SCHEDULED").update(
            astatus="NOSHOW"
        )
        apast = Appointment.objects.filter(adate__lt=today).order_by("adate", "atime")
        apresent = Appointment.objects.filter(adate=today).order_by("atime")
        afuture = Appointment.objects.filter(adate__gt=today).order_by("adate", "atime")

        # print(appointment)
        data = {"apast": apast, "apresent": apresent, "afuture": afuture}
        # data={'appointment':appointment}
        return render(request, "admin/appointment/manageappointment.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def astatus(request, aid):
    if request.user.is_authenticated and request.user.is_admin:
        appointment = Appointment.objects.get(aid=aid)

        if request.method == "POST":
            astatus = request.POST.get("astatus")
            appo = Appointment.objects.filter(aid=aid).update(astatus=astatus)

            email = appointment.cid.email
            subject = "Your Appointment is cancel"
            message = "<br>* Appointment Date " + str(appointment.adate)
            message = message + f"\n<br>* Appointment Time =  {appointment.atime}"
            message = (
                message + f"\n<br>* Selected Barbar = {appointment.eid.first_name}"
            )
            message = (
                message + f"\n<br>* Appintment Service Price = {appointment.aprice}"
            )
            message = mark_safe(message)
            send_email(email, subject, message)
            messages.success(request, "Appointment Successfully Canceled..")
            return redirect("/admin/appointment/manageappointment/")

        return render(
            request,
            "admin/appointment/manageastatus.html",
            {"appointment": appointment},
        )
    else:
        return redirect("home")


@login_required(login_url="/")
def manageorder(request):
    if request.user.is_authenticated and request.user.is_admin:
        # orderitem =OrderItem.objects.all()
        dorder = Order.objects.filter(delivered_status="YES").order_by("-oid")
        order = Order.objects.filter(delivered_status="NO").order_by("-oid")
        data = {"order": order, "dorder": dorder}
        # if request.method=='POST':

        return render(request, "admin/order/manageorder.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def vieworder(request, oid):
    if request.user.is_authenticated and request.user.is_admin:
        order = Order.objects.get(oid=oid)
        orderitem = OrderItem.objects.filter(oid=oid)
        data = {"orderitem": orderitem, "order": order}
        print(data)
        if request.method == "POST":
            delivered_status = request.POST.get("delivered_status")
            order.delivered_status = delivered_status
            if delivered_status == "YES":
                order.save()
                email = order.cid.email
                for i in orderitem:
                    stock = i.pid.pstock - i.quantity
                    product = Product.objects.filter(pid=i.pid.pid).update(pstock=stock)
                order.order_place_date = date.today()

                subject = "Your Order Is Delivered"
                message = f"\n <br>Order Id = {order.oid} \n"
                message = message + f"\n <br>Order Amount =  {order.total_amount}"
                message = (
                    message + f"\n<br>|| Product Name | Quantity | Price | Total ||"
                )

                for p in orderitem:
                    pname = p.pid.pname
                    pprice = p.pid.pprice
                    quantity = p.quantity

                    message = (
                        message
                        + f"\n<br> {pname}  | {quantity}  | {pprice}  | {quantity * pprice}"
                    )
                message = mark_safe(message)
                send_email(email, subject, message)

            messages.success(request, "Your Order is is succesfully updated ")
            return redirect("/admin/order/manageorder/")

        return render(request, "admin/order/vieworder.html", data)
    else:
        return redirect("home")


# profile
@login_required(login_url="/")
def adminprofile(request):
    if request.user.is_authenticated and request.user.is_admin:
        uid = request.user
        user = User.objects.get(id=request.user.id)

        return render(request, "admin/adminprofile.html", {"user": user})
    else:
        return redirect("home")


@login_required(login_url="/")
def admineditprofile(request):
    if request.user.is_authenticated and request.user.is_admin:
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

            return redirect("adminprofile")

        return render(request, "admin/admineditprofile.html", {"user": user})
    else:
        return redirect("home")


#  leave manage


@login_required(login_url="/")
def manageleave(request):
    if request.user.is_authenticated and request.user.is_admin:
        leave = Leave.objects.filter(
            Q(lstatus="APPROVAL") | Q(lstatus="NOTAPPROVAL")
        ).order_by("-lid")
        leavepending = Leave.objects.filter(Q(lstatus="PENDING")).order_by("-lid")
        data = {"leave": leave, "leavepending": leavepending}
        return render(request, "admin/leave/manageleave.html", data)
    else:
        return redirect("home")


@login_required(login_url="/")
def editleave(request, lid):
    if request.user.is_authenticated and request.user.is_admin:
        leave = Leave.objects.get(lid=lid)

        data = {"leave": leave}
        if request.method == "POST":
            lstatus = request.POST.get("lstatus")
            leave.lstatus = lstatus
            leave.save()
            messages.success(request, "Your Leave is is succesfully Updated ")
            return redirect("/admin/leave/manageleave/")

        return render(request, "admin/leave/editleave.html", data)
    else:
        return redirect("home")
