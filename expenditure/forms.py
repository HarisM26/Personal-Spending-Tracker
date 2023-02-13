from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

class LogInForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
    
   
    def save(self,):
        super().save(commit=False)
        user=User.objects.create_user(
            self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            

            
        )
        return user
