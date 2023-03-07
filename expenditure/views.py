from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from .news_api import all_articles
from django.core.files.storage import FileSystemStorage
from django.urls import reverse,reverse_lazy
from .models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from decimal import *
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist


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

def spending(request):
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
    return render(request, 'spending.html',context)


class CreateCategoryView(LoginRequiredMixin,CreateView):
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

    def form_invalid(self, form):
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
    

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user_profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
    
    return render(request, 'profile.html', {'user_form': user_form})


def log_out(request):
    logout(request)
    return redirect('home')

def news_page(request):
    articles = all_articles['articles']
    return render(request, 'news_page.html',{'articles':articles})   

def add_transaction(request,request_id):
    category = get_object_or_404(Category, id=request_id)
    category_limit = category.limit

    if category.is_income:
        create_transaction_form = IncomingForm
    else:
        create_transaction_form = SpendingForm

    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({'category': category.pk})
        create_transaction_form = create_transaction_form(updated_request, request.FILES)
        if create_transaction_form.is_valid():
            # transaction = create_transaction_form.save(commit=False)
            # transaction.category = category
            # category_limit.addSpentAmount(transaction.amount)
            # category_limit.save()
            # transaction.save()
            transaction = create_transaction_form.save()
            return HttpResponseRedirect(reverse('spending'))
    else:
        create_transaction_form = create_transaction_form()   
    
    context = {
        'request_id': request_id,
        'create_transaction_form': create_transaction_form,
    }

    return render(request, 'add_transaction.html', context)

def list_incomings(request):
    incomings = Transaction.incomings.all()
    context = {
        'incomings': incomings,
    }
    return render(request, 'incomings.html', context=context)

def get_total_transactions_by_date(request, from_date, to_date):
    return Transaction.spendings.filter(
        date__gte=from_date,
        date__lte=to_date,
        category__user=request.user
    ).annotate(month=TruncMonth("date")).values("month").annotate(total=Sum("amount")).values("month", "total")

def view_report(request):
    from_date = date(date.today().year-1, date.today().month, 1)
    to_date = date.today()

    if request.method == "POST":
        form = DateReportForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get("from_date")
            to_date = form.cleaned_data.get("to_date")
    else:
        form = DateReportForm(initial={
            "from_date": from_date,
            "to_date": to_date
        })
    
    transactions = get_total_transactions_by_date(request, from_date, to_date)

    context = {
        "form": form,
        "transactions": transactions,
    }
    return render(request, 'report.html', context=context)

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

def leaderboard(request):
    return render(request, 'leaderboard.html')

def profile(request):
    return render(request, 'profile.html')

def reports(request):
    return render(request, 'reports.html')


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
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
                
def friends(request):
    if request.method == 'GET':
        query=request.GET.get('q')
        
        submitbutton=request.GET.get('submit')
        
        if query is not None:
            lookups=Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)
            
            results= User.objects.filter(lookups).distinct()
            
            context={'results': results, 'submitbutton': submitbutton}
            
            return render(request, 'friends.html', context)
            
        else:
            return render(request, 'friends.html')
            
    else:
            return render(request, 'friends.html') 
            
def show_friends_profile(request, id):
    results = User.objects.get(id = id)
    template = loader.get_template('friends_profile.html')
    context = {
        'results': results,
    }
    return HttpResponse(template.render(context, request))

@login_required    
def follow_toggle(request, id):
    current_user = request.user
    try:
        followee = User.objects.get(id=id)
        current_user.toggle_follow(followee)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return redirect('friends_profile', id=id)
    

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = 'Successfully changed password'
    success_url = reverse_lazy("user_profile")

def forgot_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
    else:
        form = EmailForm()
    return render(request, 'forgot_password.html', {'form': form})