from django.db import models
from myapp.models import User
import os

# Create your models here.


class Service(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=50)
    sprice = models.IntegerField(default=0)
    sdesc = models.CharField(max_length=500, default="")
    simg = models.ImageField(upload_to="service/images", default="")

    def __str__(self):
        return self.sname

    def delete(self, *args, **kwargs):
        # delete the file from the file system
        if self.simg:
            os.remove(self.simg.path)

        # call the parent class delete method to delete the object
        super(Service, self).delete(*args, **kwargs)


class Appointment(models.Model):
    aid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    sid = models.ManyToManyField(Service)
    adate = models.DateField()
    atime = models.TimeField()
    eid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    aduration = models.DurationField()
    aprice = models.IntegerField(default=10)
    mobile_no = models.CharField(max_length=13)
    STATUS_CHOICES = (
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCEL", "Cancel"),
        ("NOSHOW", "NoShow"),
    )
    astatus = models.CharField(max_length=10, choices=STATUS_CHOICES)


class Holidays(models.Model):
    hid = models.AutoField(primary_key=True)
    hdesc = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
