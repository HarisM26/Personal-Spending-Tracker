from django import forms
from expenditure.models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import datetime, date
from .models import Transaction
from .helpers import not_future
from betterforms.multiform import MultiModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SpendingTransactionForm(forms.ModelForm):
    class Meta:
        model = SpendingTransaction
        fields = '__all__'
        exclude = ('spending_category','is_current',)
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

class IncomeTransactionForm(forms.ModelForm):
    class Meta:
        model = IncomeTransaction
        fields = '__all__'
        exclude=('income_category',)
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
class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model=IncomeCategory
        fields = ('name',)

class SpendingCategoryForm(forms.ModelForm):
    class Meta:
        model = SpendingCategory
        fields = ('name',)

class LimitForm(forms.ModelForm):
    class Meta:
        model = Limit
        fields = '__all__'
        exclude = ('remaining_amount','status','end_date')
    
class CategoryCreationMultiForm(MultiModelForm):
    form_classes = {
        'category': SpendingCategoryForm,
        'limit': LimitForm
    }

class SpendingCategoryEditMultiForm(MultiModelForm):
    form_classes = {
        'category': SpendingCategoryForm,
        'limit': LimitForm
    }


class LogInForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

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


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, label='first_name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label='last_name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class DateReportForm(forms.Form):
    from_date = forms.DateField(label="from", validators=[not_future], widget=DatePickerInput(options={"format": "DD/MM/YYYY"}))
    to_date = forms.DateField(label="to", validators=[not_future], widget=DatePickerInput(options={"format": "DD/MM/YYYY"}))


