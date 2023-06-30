from django.contrib.auth.forms import UserCreationForm, UserChangeForm  
from django.db.models import fields  
from django import forms  
from .models import User
from django.contrib.auth import get_user_model  
  
User = get_user_model()  
  
class CustomUserCreationForm(UserCreationForm):  
  
    password1 = forms.CharField(widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)  
    first_name = forms.CharField(label="First Name",widget=forms.TextInput)
    last_name = forms.CharField(label="Last Name",widget=forms.TextInput)
    phone = forms.CharField(label="Phone No",widget=forms.TextInput,max_length=20)
      
    class Meta:  
        model = User  
        fields = ('email', )  
      
    def clean_email(self):  
        email = self.cleaned_data.get('email')  
        qs = User.objects.filter(email=email)  
        if qs.exists():  
            raise forms.ValidationError("Email is taken")  
        return email  
  
    def clean(self):  
        '''  
        Verify both passwords match.  
        '''  
        cleaned_data = super().clean()  
        password1 = cleaned_data.get("password1")  
        password2 = cleaned_data.get("password2")  
          
        if password1 is not None and password1 != password2:  
            self.add_error("password2", "Your passwords must match")  
        return cleaned_data  
  
    def save(self, commit=True):  
        # Save the provided password in hashed format  
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data["password1"])  
        if commit:  
            user.save()  
        return user          
      
  
# class CustomUserChangeForm(UserChangeForm):  
#     class Meta:  
#         model = User  
#         fields = ('email', )  
  
#     def clean_password(self):  
#         # Regardless of what the user provides, return the initial value.  
#         # This is done here, rather than on the field, because the  
#         # field does not have access to the initial value  
#         return self.initial["password1"] 


