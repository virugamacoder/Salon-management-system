from django.contrib import admin
from .models import *
 
# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Feedback)
