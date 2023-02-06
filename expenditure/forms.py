import datetime
from django import forms
from django.forms import ModelForm

from expenditure.models import Category

class CategoryMeta():
    model = Category
    fields = ['name', 'categorical_limit']




class CategoryForm(forms.Form):
    
    class Meta(CategoryMeta):
        pass

    