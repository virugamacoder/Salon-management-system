from django.conf import settings
from django.shortcuts import get_object_or_404
from employee.models import User_Employee
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
import pyotp
from django.contrib.auth.decorators import login_required
from appointment.models import Service
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static


from myapp.models import OTP


def custom_404_view(request, exception):
    return render(request, "myapp/404-page.html", status=404)


# Create your views here.
User = get_user_model()
# ---------email-------------------------------

# --------------------------------------------------


def index(request):
    data = {}
    barbar = User_Employee.objects.all()[:3]
    data["barbar"] = barbar
    if request.user.is_authenticated:
        data["user"] = request.user

    return render(request, "myapp/index.html", data)


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect("home")
    else:
        return redirect("home")


def loginhandle(request):
    data = {}

    if request.method == "POST":
        loginemail = request.POST.get("loginemail", "")
        loginpassword = request.POST.get("loginpass", "")
        user = authenticate(email=loginemail, password=loginpassword)

        print(loginemail)
        print(loginpassword)

        if user is not None:
            login(request, user)
            username = request.user.first_name
            mymsg = "Successfully Logged In " + username
            messages.success(request, mymsg)
            request.session["user_id"] = user.id
            if request.user.is_customer:
                return redirect("home")
            elif request.user.is_employee:
                return redirect("edashboard")
            elif request.user.is_admin:
                return redirect("dashboard")

        else:
            messages.error(request, "Invalid Email address or Password !")
            # return redirect("loginpage")
            data = {}
            data["loginemail"] = loginemail
            data["loginpass"] = loginpassword
            return render(request, "myapp/login.html", data)

    return HttpResponse("404- Not found")
    # return HttpResponse("login")
    # return redirect('home')
    # return render(request,"/myapp/index.html")


def signuphandle(request):
    if request.method == "POST":
        fname = request.POST.get("fname", "")
        lname = request.POST.get("lname", "")
        email = request.POST.get("email", "")
        pass1 = request.POST.get("pass1", "")
        pass2 = request.POST.get("pass2", "")

        if pass1 == pass2:
            try:
                user = User.objects.filter(email=email).first()

                if user:
                    messages.error(
                        request,
                        "Email ID User Already associated with an account Please Use Different Email Id ",
                    )
                    data["fname"] = fname
                    data["lname"] = lname
                    data["pass1"] = pass1
                    data["pass2"] = pass2
                    # return redirect("/signup/")
                    return render(request, "myapp/signup.html", data)

                else:
                    subject = "OTP Verification For Complate Registration"
                    message = "Your Otp Is "
                    otp = generate_otp(email, subject, message)
                    print("otp : ", otp)
                    request.session["signup_data"] = {
                        "email": email,
                        "fname": fname,
                        "lname": lname,
                        "password": pass1,
                        "otp": otp,
                    }
                    return redirect("/otppage/")
            except Exception as e:
                messages.error(request, e)
                return redirect("/signup/")
        else:
            msg = "Password and Confirm Password did not match"
            messages.error(request, msg)
            # return redirect("/signup/")
            data = {}
            data["fname"] = fname
            data["lname"] = lname
            data["email"] = email
            data["pass1"] = pass1
            data["pass2"] = pass2
            return render(request, "myapp/signup.html", data)

    else:
        messages.error(request, "Somthing Wrong")
        return redirect("home")


def otppage(request):
    if "signup_data" in request.session:
        return render(request, "myapp/otppage.html")
    return redirect("home")


def generate_otp(email, subject, message):
    totp = pyotp.TOTP("base32secret3232")
    otp_value = totp.now()
    message = message + otp_value
    send_otp_email(email, subject, message)
    return otp_value


def send_otp_email(email, subject, message):
    # logo_url = request.build_absolute_uri(settings.STATIC_URL + "images/logo.png")
    logo_url = "images/logo-default-dark-200x36.png"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    html_message = render_to_string(
        "email_templates/email.html",
        {"subject": subject, "message": message, "logo_url": logo_url},
    )
    mail = EmailMultiAlternatives(subject, "", from_email, recipient_list)
    mail.attach_alternative(html_message, "text/html")
    mail.send()


def otpvalidate(request):
    if "signup_data" in request.session:
        otp = request.session["signup_data"]["otp"]
        if request.method == "POST":
            i1 = request.POST.get("otpi1", "")
            i2 = request.POST.get("otpi2", "")
            i3 = request.POST.get("otpi3", "")
            i4 = request.POST.get("otpi4", "")
            i5 = request.POST.get("otpi5", "")
            i6 = request.POST.get("otpi6", "")

            reciveotp = i1 + i2 + i3 + i4 + i5 + i6
            try:
                if otp == reciveotp:
                    user = User.objects._create_user(
                        email=request.session["signup_data"]["email"],
                        password=request.session["signup_data"]["password"],
                        first_name=request.session["signup_data"]["fname"],
                        last_name=request.session["signup_data"]["lname"],
                        is_customer=True,
                    )
                    del request.session["signup_data"]
                    messages.success(request, "Otp Validate Successfully signup ")
                    return redirect("loginpage")
                else:
                    messages.error(request, "Otp Not Validate")
                    data = {}
                    data["i1"] = i1
                    data["i2"] = i2
                    data["i3"] = i3
                    data["i4"] = i4
                    data["i5"] = i5
                    data["i6"] = i6
                    return render(request, "myapp/otppage.html", data)
            except Exception as e:
                messages.error(request, e)
                return redirect("home")
        else:
            return redirect("home")
    return redirect("home")


def delete_otp(user):
    pyotp.OTP.objects.filter(user=user).delete()


def about(request):
    data = {}
    barbar = User_Employee.objects.all()[:3]
    data["barbar"] = barbar
    return render(request, "myapp/about.html", data)


def contacts(request):
    return render(request, "myapp/contacts.html")


def barbers(request):
    data = {}
    # barbar = User.objects.filter(is_employee=True)
    barbar = User_Employee.objects.all()
    data["barbar"] = barbar
    return render(request, "myapp/barbers.html", data)


def services(request):
    service = Service.objects.all()
    data = {}
    data["service"] = service
    print("data  : ", data)
    return render(request, "myapp/services.html", data)


def loginpage(request):
    if request.user.is_authenticated:
        if request.user.is_employee:
            return redirect("edashboard")
        if request.user.is_admin:
            return redirect("dashboard")

        return redirect("home")
    else:
        return render(request, "myapp/login.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request, "myapp/signup.html")


def otppage2(request):
    return render(request, "myapp/otppage2.html")


def otppage2(request):
    if "resetotp" in request.session and "resetemail" in request.session:
        return render(request, "myapp/otppage2.html")
    else:
        return redirect("home")


def resetpass1(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        try:
            user = User.objects.get(email=email)
            subject = "OTP Verification To Forgot Password"
            message = "Your Otp Is "
            otp = generate_otp(email, subject, message)
            print("otp : ", otp)
            request.session["resetemail"] = email
            request.session["resetotp"] = otp
            return redirect("/otppage2/")

        except User.DoesNotExist:
            messages.error(
                request,
                "Email Id Is Not Registration.",
            )
            data = {}
            data["email"] = email
            return render(request, "myapp/resetpass1.html", data)

        return redirect("/resetpass1/")

    return render(request, "myapp/resetpass1.html")


def resetpassvalidate(request):
    if "resetotp" in request.session and "resetemail" in request.session:
        otp = request.session["resetotp"]
        if request.method == "POST":
            i1 = request.POST.get("otpi1", "")
            i2 = request.POST.get("otpi2", "")
            i3 = request.POST.get("otpi3", "")
            i4 = request.POST.get("otpi4", "")
            i5 = request.POST.get("otpi5", "")
            i6 = request.POST.get("otpi6", "")

            reciveotp = i1 + i2 + i3 + i4 + i5 + i6
            try:
                if otp == reciveotp:
                    del request.session["resetotp"]
                    messages.success(
                        request, "Otp Validate Successfully Reset The Password"
                    )
                    return redirect("/resetpass2/")
                else:
                    messages.error(request, "Otp Not Validate")
                    return redirect("/resetpass1/")
            except Exception as e:
                messages.error(request, e)
                return redirect("/resetpass1/")

    return redirect("home")


def resetpass2(request):
    if "resetemail" in request.session:
        if request.method == "POST":
            pass1 = request.POST.get("pass1")
            pass2 = request.POST.get("pass2")

            if pass1 == pass2:
                email = request.session["resetemail"]
                user = User.objects.get(email=email)

                user.set_password(pass1)
                user.save()
                del request.session["resetemail"]
                messages.success(request, "Password Successfully Reset..")
                return redirect("/login/")
            else:
                messages.error(
                    request, "New Password And Confirm New Password Not Same !"
                )
                return redirect("/resetpass2/")
        return render(request, "myapp/resetpass2.html")
    return redirect("home")
