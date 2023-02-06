from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Transaction, User
from .forms import TransactionForm, LogInForm, SignUpForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def features(request):
    return render(request, 'features.html')

def log_out(request):
    logout(request)
    return redirect('home')

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")

    return render(request, 'log_in.html', {'form': LogInForm()})

    




def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html' , {'form': form})



def addTransaction(request):
    if request.method == 'POST':
        create_transaction_form = TransactionForm(request.POST, request.FILES)
        if create_transaction_form.is_valid():
            create_transaction_form.save()
            return HttpResponseRedirect(reverse('transactions'))
    else:
        create_transaction_form = TransactionForm()
   
    context = {
        'create_transaction_form': create_transaction_form
    }
    return render(request, 'add_transaction.html', context=context)

def listTransactions(request):
    transactions = Transaction.objects.all()

    context = {
        'transactions': transactions,
    }

    return render(request, 'transactions.html', context=context)