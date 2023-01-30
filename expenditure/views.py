from django.shortcuts import redirect, render
from .forms import LogInForm, SignUpForm
from .models import User



def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def features(request):
    return render(request, 'features.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html' , {'form': form})


def log_in(request):
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})
