from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from datetime import datetime, date
from .models import User, Transaction
from .helpers import not_future

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('title', 'date', 'amount', 'notes', 'is_income', 'reciept', 'category')

    def clean_transaction_availability(self):
        transaction_date = self.cleaned_data.get('date')
        current_date = date.today()
        if transaction_date > current_date:
            self.add_error('date', 'The date of your transaction cannot be in the future')
        return transaction_date    

class LogInForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    #new_password = forms.CharField(label='Password', widget=forms.PasswordInput(), validators=[RegexValidator(
        #regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
        #message='Password must contain an uppercase character, a lowercase character and a number'
    #)]

    
    
    #)
    #password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation =self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'confirmation does not match password')

    
    def save(self):
        super().save(commit=False)
        user=User.objects.create_user(
            self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            

            
        )
        return user
