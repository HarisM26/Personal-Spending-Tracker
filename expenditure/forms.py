from django import forms
from expenditure.models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User, Transaction
from bootstrap_datepicker_plus.widgets import DatePickerInput

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ('category',)
        widgets = {'date': DatePickerInput(options={"format": "DD/MM/YYYY"})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','is_income')

    limit = forms.DecimalField(label='Spending Limit')

class LogInForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    new_password = forms.CharField(label='Password', widget=forms.PasswordInput(), validators=[RegexValidator(
        regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
        message='Password must contain an uppercase character, a lowercase character and a number'
    )])
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation =self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'confirmation does not match password')

    def save(self):
        super().save(commit=False)
        self.user=User.objects.create_user(
            email = self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'), 
            password=self.cleaned_data.get('new_password'),
        )
        return self.user
