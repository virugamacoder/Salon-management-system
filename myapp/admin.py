from django.contrib import admin
from .models import *
from django.contrib.auth import authenticate  
from django.contrib.auth.admin import UserAdmin 
from .forms import *

# Register your models here.

admin.site.register(Test)

# admin.site.register(Customer1)
admin.site.register(Admin)


class CustomUserAdmin(UserAdmin):  
    add_form = CustomUserCreationForm  
    # form = CustomUserChangeForm  
    model = User  
  
    list_display = ('email', 'is_staff', 'is_active','is_employee','is_customer','is_admin')  
    list_filter = ('email', 'is_staff', 'is_active','is_employee','is_customer','is_admin')
      
    fieldsets = (  
        ('Change For User Detalis ', {'fields': ('email', 'password','first_name','last_name','phone','uimg')}),  
        ('Permissions', {'fields': ('is_staff', 'is_active','is_employee','is_customer','is_admin')}),  
    )  
    
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('email', 'password1', 'password2','first_name', 'last_name','phone','uimg','is_staff', 'is_active','is_employee','is_customer','is_admin')}  
        ),  
    )  
    
    search_fields = ('email',)  
    
    ordering = ('email',)  
    
    filter_horizontal = ()  
  
admin.site.register(User, CustomUserAdmin)  






