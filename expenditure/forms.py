from django import forms
from expenditure.models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import datetime, date
from .models import User, Transaction

class SpendingForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'date': DatePickerInput(options={"format": "DD/MM/YYYY"}),
            'category': forms.HiddenInput(),
            }

    # def clean_spending_date(self):
    #     spending_date = self.cleaned_data.get('date')
    #     current_date = date.today()
    #     if spending_date > current_date:
    #         self.add_error('date', 'The date of your outgoing outgoing transaction cannot be in the future')
    #     return spending_date

class IncomingForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ('reciept',)
        widgets = {
            'date': DatePickerInput(options={"format": "DD/MM/YYYY"}),
            'category': forms.HiddenInput(),
            }

    # def clean_incoming_date(self):
    #     incoming_date = self.cleaned_data.get('date')
    #     current_date = date.today()
    #     if incoming_date > current_date:
    #         self.add_error('date', 'The date of your incoming transaction cannot be in the future')
    #     return incoming_date    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','limit')

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
