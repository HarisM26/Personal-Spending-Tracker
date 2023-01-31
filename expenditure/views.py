from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def contact(request):
    return render(request, 'contact.html')

def feed(request):
    return render(request, 'feed.html')

def news_page(request):
    return render(request, 'news_page.html')

def notification_page(request):
    return render(request, 'notification_page.html')


def register(request):
    if request.method == 'POST':
        # request.POST contains dictionary with all of the data
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def create_category(request):
    if request.method == 'POST':
        # request.POST contains dictionary with all of the data
        if request.user.is_authenticated:
            current_user = request.user
            form = CategoryForm(request.POST)
            if form.is_valid():
                name=form.cleaned_data.get('name')
                limit=form.cleaned_data.get('limit')
                category = Category.objects.create(user=current_user,name=name,limit=limit)
                messages.add_message(request, messages.SUCCESS,
                             "Category created!")
                return redirect('create_category')
            messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
        else:
            return redirect('log_in')
    else:
        form = CategoryForm()
        return render(request, 'create_category.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        # Add error message here
        messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
    else:
        form = LogInForm()
        return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')