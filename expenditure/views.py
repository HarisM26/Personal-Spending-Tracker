from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from .news_api import all_articles
from django.core.files.storage import FileSystemStorage
from django.urls import reverse,reverse_lazy
from .models import *
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def contact(request):
    return render(request, 'contact.html')


def get_unread_nofications(user):
    return Notification.objects.filter(user_receiver = user,status = 'unread').count()

def get_user_notifications(user):
    return Notification.objects.filter(user_receiver = user)

def feed(request):
    current_user = request.user
    unread_status_count = get_unread_nofications(current_user)
    notifications = get_user_notifications(current_user)
    latest_notifications = notifications[0:3]
    context = {
        'latest_notifications': latest_notifications,
        'unread_status_count': unread_status_count,
    }
    return render(request, 'feed.html', context)

def notification_page(request):
    current_user = request.user
    notifications = get_user_notifications(current_user)
    latest_notifications = notifications[0:3]
    unread_status_count = get_unread_nofications(current_user)
    context = {
        'latest_notifications': latest_notifications,
        'notifications': notifications,
        'unread_status_count': unread_status_count,
    }
    return render(request, 'notification_page.html',context)

def mark_as_read(request,id):
   notification = Notification.objects.get(id=id)
   notification.status = 'read'
   notification.save()
   return redirect('notification_page') 

def all_categories(request):
    current_user = request.user
    categories = Category.objects.filter(user = current_user)
    notifications = get_user_notifications(current_user)
    latest_notifications = notifications[0:3]
    unread_status_count = get_unread_nofications(current_user)
    context = {
        'latest_notifications': latest_notifications,
        'categories':categories,
        'unread_status_count': unread_status_count,
        }
    return render(request, 'all_categories.html',context)

def sign_up(request):
    if request.method == 'POST':
        # request.POST contains dictionary with all of the data
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

#def create_category(request):
#    current_user = request.user
#    notifications = get_user_notifications(current_user)
#    latest_notifications = notifications[0:3]
#    unread_status_count = get_unread_nofications(current_user)
#    if request.method == 'POST':
#        # request.POST contains dictionary with all of the data
#        if request.user.is_authenticated:
#            form = CategoryForm(request.POST)
#            if form.is_valid():
#                name=form.cleaned_data.get('name')
#                limit=form.cleaned_data.get('limit')
#                category = Category.objects.create(user=current_user,name=name,limit=limit)
#                messages.add_message(request, messages.SUCCESS,
#                             "Category created!")
#                return redirect('create_category')
#            messages.add_message(request, messages.ERROR,
#                             "The credentials provided were invalid!")
#        else:
#            return redirect('log_in')
#    else:
#        form = CategoryForm()
#    context = {
#        'form': form,
#        'latest_notifications': latest_notifications,
#        'unread_status_count': unread_status_count,
#    }
#    return render(request, 'create_category.html', context)

class CategoryView(LoginRequiredMixin,CreateView):
    template_name = "create_category.html"
    form_class = CategoryCreationMultiForm
    #success_url = reverse_lazy('create_category')

    def form_valid(self, form):
        limit = form['limit'].save(commit=False)
        limit.remaining_amount = limit.limit_amount
        limit.save()
        category = form['category'].save(commit=False)
        category.user = self.request.user
        category.limit = limit
        category.save()
        messages.add_message(self.request, messages.SUCCESS,
                                "Category created!")
        return redirect('create_category')

    def form_valid(self, form):
        messages.add_message(self.request, messages.ERROR,
                                "Your input is invalid!, try again")
        return redirect('create_category')
    
    def creation_view(self):
        current_user = self.request.user
        notifications = get_user_notifications(current_user)
        latest_notifications = notifications[0:3]
        unread_status_count = get_unread_nofications(current_user)
        context = {
            'latest_notifications': latest_notifications,
            'unread_status_count': unread_status_count,
        }
        return context
    
    #    if request.method == 'POST':
    #        # request.POST contains dictionary with all of the data
    #        if request.user.is_authenticated:
    #            form = self.form_class
    #            form.cleaned_data['user']=current_user
    #            
    #            if form.is_valid():
    #                form.save()
    #                #name=form.cleaned_data.get('name')
    #                #limit=form.cleaned_data.get('limit')
    #                #category = Category.objects.create(user=current_user,name=name,limit=limit)
    #                messages.add_message(request, messages.SUCCESS,
    #                             "Category created!")
    #                return redirect('create_category')
    #            messages.add_message(request, messages.ERROR,
    #                             "You provided invalid input!")
    #        else:
    #            return redirect('log_in')
    #    else:
    #        form = CategoryForm()
    #    
    #    return render(request, 'create_category.html', context)

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
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

def news_page(request):
    articles = all_articles['articles']
    return render(request, 'news_page.html',{'articles':articles})   

def add_transaction(request,request_id):
    category = Category.objects.get(id=request_id)
    if request.method == 'POST':
        create_transaction_form = TransactionForm(request.POST, request.FILES)
        if create_transaction_form.is_valid():
            transaction = create_transaction_form.save(commit=False)
            transaction.category = category
            transaction.save()
            return HttpResponseRedirect(reverse('all_categories'))
    else:
        create_transaction_form = TransactionForm()   
    context = {
        'request_id': request_id,
        'create_transaction_form': create_transaction_form,
    }
    return render(request, 'add_transaction.html', context)

def list_transactions(request):
    transactions = Transaction.objects.all()
    context = {
        'transactions': transactions,
    }
    return render(request, 'transactions.html', context=context)

def view_settings(request):
    current_user = request.user
    toggle = current_user.toggle_notification
    return render(request,'settings.html',{'toggle':toggle})

def toggle_notification(request):
    current_user = request.user
    if current_user.toggle_notification == 'ON':
        current_user.toggle_notification='OFF'
        current_user.save()
    else:
        current_user.toggle_notification='ON'
        current_user.save()
    return redirect('settings')
    
