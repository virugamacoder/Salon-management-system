from datetime import timezone
from django.db import models
from appointment.models import Service
import os

from myapp.models import User

# Create your models here.


class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50)
    pprice = models.IntegerField(default=0)
    pdesc = models.CharField(max_length=1000, default="")
    pinfo = models.CharField(max_length=1000, default="")
    pstock = models.IntegerField(default=0)
    pimg = models.ImageField(upload_to="shop/images", null=True, blank=True)

    def __str__(self):
        return self.pname

    def delete(self, *args, **kwargs):
        # delete the file from the file system
        if self.pimg:
            os.remove(self.pimg.path)

        # call the parent class delete method to delete the object
        super(Product, self).delete(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Address(models.Model):
    aid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(User, on_delete=models.CASCADE)
    rname = models.CharField(max_length=50)
    contactno = models.CharField(max_length=10)
    address = models.CharField(max_length=700)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    locality = models.CharField(max_length=50, default="")
    postcode = models.CharField(max_length=6)

    def __str__(self):
        return self.rname


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(User, on_delete=models.CASCADE)
    aid = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_place_date = models.DateField()
    payment_mode = models.CharField(max_length=50, default="COD")
    payment_date = models.DateField()
    total_amount = models.FloatField()
    transaction_id = models.CharField(max_length=50)
    delivered_CHOICES = (
        ("YES", "Delivered"),
        ("NO", "Not Deliverd"),
    )
    delivered_status = models.CharField(max_length=10, choices=delivered_CHOICES)

    # new Table


class OrderItem(models.Model):
    order_d_id = models.AutoField(primary_key=True)
    oid = models.ForeignKey(Order, on_delete=models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=False)
    price = models.FloatField(default=1, null=False)


class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(User, on_delete=models.CASCADE)
    sid = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    fdesc = models.CharField(max_length=500)
    fdate = models.DateField()
