from django import forms
from django.core.validators import RegexValidator
from expenditure.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    new_password = forms.CharField(label='Password',
                                   widget=forms.PasswordInput(),
                                   validators=[RegexValidator(
                                       regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                                       message='Password must contain uppercase character, a lowercase'
                                       'character and a number'
                                   )]
                                   )
    confirm_password = forms.CharField(
        label='confirm_password', widget=forms.PasswordInput())

    """clean is used to access password and compare the 2"""

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

    # Saves the user to the database
    def save(self):
        super().save(commit=False)
        self.user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return self.user


class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
