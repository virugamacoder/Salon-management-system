from django.db import models
from myapp.models import User
from datetime import timedelta
from django.utils import timezone
# Create your models here.


class User_Employee(models.Model):
    emp = models.OneToOneField(User, on_delete=models.CASCADE)
    infromation = models.CharField(max_length=300, default="")
    skills = models.CharField(max_length=100, default="")


class Leave(models.Model):
    lid = models.AutoField(primary_key=True)
    eid = models.ForeignKey(User, on_delete=models.CASCADE)
    lreson = models.CharField(max_length=200)
    lstart_date = models.DateField()
    lend_date = models.DateField()
    ldays = models.PositiveIntegerField(default=0)

    LEAVE_CHOICES = (
        ("APPROVAL", "Approval"),
        ("NOTAPPROVAL", "Not approval"),
        ("PENDING", "Pending"),
    )
    lstatus = models.CharField(max_length=15, choices=LEAVE_CHOICES, default="PENDING")
