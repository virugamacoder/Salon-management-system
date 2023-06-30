from decimal import Decimal
from datetime import date, timedelta
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product, Address, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static
import razorpay


# Create your views here.


def shop(request):
    products = Product.objects.all()
    count = 0
    data = {}

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)

        if carts.exists():
            cart = carts.first()
            cart_items = CartItem.objects.filter(cart=cart)
            count = cart_items.count()
            data["count"] = count
            data["itemcart"] = cart_items

    data["count"] = count
    data["products"] = products
    print(data)
    return render(request, "shop/shop.html", data)


def single_prod(request, pid):
    product = Product.objects.get(pid=pid)
    product1 = Product.objects.all()[:3]
    data = {}
    data["product"] = product
    data["product1"] = product1
    return render(request, "shop/single-product.html", data)


def cart(request):
    if request.user.is_authenticated and request.user.is_customer:
        carts = Cart.objects.filter(user=request.user)
        data = {}

        total = 0
        if carts.exists():
            cart = carts.first()
            cart_items = CartItem.objects.filter(cart=cart)
            print(cart)

            for i in cart_items:
                total = total + ((i.product.pprice) * (i.quantity))
            print(total)

            data["cart_items"] = cart_items
            data["total"] = total
            return render(request, "shop/cart.html", data)
        else:
            return render(request, "shop/cart.html")
    else:
        messages.error(request, "View Cart Is Must User Login Required ! Please Login")
        return redirect("loginpage")


def addcart(request, pid):
    if request.user.is_authenticated and request.user.is_customer:
        product = get_object_or_404(Product, pid=pid)
        print(product)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        shopredirect = "/s/shop/#product-" + str(pid)
        print(shopredirect)
        return redirect(shopredirect)
    else:
        messages.error(
            request, "Add To Cart Is Must User Login Required ! Please Login"
        )
        return redirect("loginpage")


@login_required(login_url="/")
def addcartplus(request, pid):
    if request.user.is_customer:
        product = get_object_or_404(Product, pid=pid)
        print(product)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect("/s/cart/")
    else:
        return redirect("home")


@login_required(login_url="/")
def removecartminus(request, pid):
    if request.user.is_customer:
        product = get_object_or_404(Product, pid=pid)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect("/s/cart/")
    else:
        return redirect("home")


@login_required(login_url="/")
def removecart(request, pid):
    if request.user.is_customer:
        product = get_object_or_404(Product, pid=pid)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return redirect("/s/cart/")
    else:
        return redirect("home")


@login_required(login_url="/")
def checkout(request):
    if request.user.is_customer:
        if request.method == "POST":
            SendTotal = request.POST.get("SendTotal")
            return render(request, "shop/checkout.html", {"SendTotal": SendTotal})
        else:
            return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="/")
def bookorder(request):
    if request.user.is_customer:
        if request.method == "POST":
            SendTotal = request.POST.get("SendTotal")
            reciever_name = (
                request.POST.get("first-name", "")
                + " "
                + request.POST.get("last-name", "")
            )
            phone = request.POST.get("phone", "")
            address = request.POST.get("address", "")
            city = request.POST.get("city", "")
            state = request.POST.get("state", "")
            postcode = request.POST.get("postcode", "")
            locality = request.POST.get("locality", "")
            payment = request.POST.get("radio-payment", "")

            # if payment == "cod":
            address_store = Address.objects.create(
                cid=request.user,
                rname=reciever_name,
                contactno=phone,
                address=address,
                city=city,
                state=state,
                postcode=postcode,
                locality=locality,
            )

            delivery_date = date.today() + timedelta(days=5)

            order = Order.objects.create(
                cid=request.user,
                aid=address_store,
                order_place_date=delivery_date,
                payment_mode=payment,
                payment_date=delivery_date,
                total_amount=SendTotal,
                delivered_status="NO",
            )
            print("order = " + order)

            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.filter(cart=cart)

            product_str = "<br> || Product Name | Quantity | Price | Total || <br>"

            for p in cart_item:
                pid = p.product
                pprice = p.product.pprice
                quantity = p.quantity
                OrderItem.objects.create(
                    oid=order, pid=pid, quantity=quantity, price=pprice
                )
                p.delete()
                # pstock = p.product.pstock - quantity
                # Product.objects.filter(pid=p.product.pid).update(pstock=pstock)
                product_str = (
                    product_str
                    + f"\n <br> {p.product.pname}  | {quantity}  | {pprice}  | {quantity * pprice}"
                )
            cart.delete()
            email = request.user.email
            subject = "Your Order is Completed !"
            orderid_msg = f"<br> * Your Order ID = {order.oid}"
            product_msg = f"<br> * Product = {product_str}"
            total_msg = f" <br> * Total Pay Rupees = {SendTotal}"
            message = orderid_msg + product_msg + total_msg
            message = mark_safe(message)
            send_email(email, subject, message)

            # return redirect("/s/finish/")

            if payment == "online":
                client = razorpay.Client(
                    auth=("rzp_test_heisFYtHc4xPw1", "DVFjuCEquZNqQm8ZaiZcDplj")
                )

                data = {
                    "amount": SendTotal,
                    "currency": "INR",
                    "reciever_name": reciever_name,
                }

                payment = client.order.create(data=data)
                print("online")

            return redirect("/s/finish/")

        else:
            return redirect("home")
    else:
        return redirect("home")


# @login_required(login_url="/")
# def payment(request):
#     if request.user.is_customer:
#         return render(request, "shop/payment.html")


@csrf_exempt
@login_required(login_url="/")
def finish(request):
    if request.user.is_customer:
        return render(request, "shop/finish.html")


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
