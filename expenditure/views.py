from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.http import HttpResponseRedirect
from .news_api import all_articles
from django.urls import reverse, reverse_lazy
from .models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from decimal import *
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import login_prohibited
from django.contrib.auth.decorators import login_required

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_prohibited
def about(request):
    return render(request, 'about.html')

@login_prohibited
def features(request):
    return render(request, 'features.html')

@login_prohibited
def contact(request):
    return render(request, 'contact.html')

def get_unread_nofications(user):
    return Notification.objects.filter(user_receiver = user,status = 'unread').count()

def get_user_notifications(user):
    return Notification.objects.filter(user_receiver = user)

@login_required
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

@login_required
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

@login_required
def mark_as_read(request,id):
   notification = Notification.objects.get(id=id)
   notification.status = 'read'
   notification.save()
   return redirect('notification_page') 

@login_required
def spending(request):
    current_user = request.user
    categories = SpendingCategory.objects.filter(user = current_user)
    notifications = get_user_notifications(current_user)
    latest_notifications = notifications[0:3]
    unread_status_count = get_unread_nofications(current_user)
    context = {
        'latest_notifications': latest_notifications,
        'categories':categories,
        'unread_status_count': unread_status_count,
        }
    return render(request, 'spending.html',context)

@login_required
def incoming(request):
    current_user = request.user
    categories = IncomeCategory.objects.filter(user = current_user)
    notifications = get_user_notifications(current_user)
    latest_notifications = notifications[0:3]
    unread_status_count = get_unread_nofications(current_user)
    context = {
        'latest_notifications': latest_notifications,
        'categories':categories,
        'unread_status_count': unread_status_count,
        }
    return render(request, 'incomings.html',context)

@login_prohibited
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

class DeleteSpendingCategoryView(LoginRequiredMixin, DeleteView):
    model = SpendingCategory
    template_name = "delete_spending_category.html"
    success_url = reverse_lazy('spending')

class DeleteIncomeCategoryView(LoginRequiredMixin, DeleteView):
    model = IncomeCategory
    template_name = "delete_income_category.html"
    success_url = reverse_lazy('incomings')

# UpdateView requirements:
# model; tell Django to update model records
# form_class; current values of category are populated in form to show user
# success_url; if update is successful go back to spending page
class EditSpendingCategoryView(LoginRequiredMixin,UpdateView):
    model = SpendingCategory
    form_class = SpendingCategoryEditMultiForm
    template_name = "edit_spending_category.html"
    success_url = reverse_lazy('spending')

    # Returns the keyword arguments for instantiating the form
    # Overriding to add category and limit to kwargs before form is created
    def get_form_kwargs(self):
        kwargs = super(EditSpendingCategoryView, self).get_form_kwargs()
        kwargs.update(instance={
            'category': self.object,
            'limit': self.object.limit,
        })
        return kwargs

    

class EditIncomeCategoryView(LoginRequiredMixin, UpdateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm
    template_name = "edit_income_category.html"
    success_url = reverse_lazy("incomings")
        

class CreateSpendingCategoryView(LoginRequiredMixin,CreateView):
    template_name = "create_category.html"
    form_class = CategoryCreationMultiForm

    def form_valid(self, form):
        limit = form['limit'].save(commit=False)
        limit.remaining_amount = limit.limit_amount
        limit.end_date = self.get_end_date(limit.time_limit_type)
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
    
    #doesnt work at the moment
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
    
    def get_end_date(self,limit_type):
        if limit_type == 'weekly':
            return datetime.date(datetime.now()) + timedelta(days=6)
        elif limit_type == 'monthly':
            return datetime.date(datetime.now()) + timedelta(days=27)
        else:
            return datetime.date(datetime.now()) + timedelta(days=364)

@login_required
def create_incoming_category(request):
    current_user = request.user
    notifications = get_user_notifications(current_user)
    latest_notifications = notifications[0:3]
    unread_status_count = get_unread_nofications(current_user)
    if request.method == 'POST':
        form = IncomeCategoryForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            incoming_category = IncomeCategory.objects.create(user=current_user,name=name)
            messages.add_message(request, messages.SUCCESS,
                             "Category created!")
            return redirect('create_incoming_category')
        messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
    else:
        form = IncomeCategoryForm()

    context = {
        'form': form,
        'latest_notifications': latest_notifications,
        'unread_status_count': unread_status_count,
    }
    return render(request, 'create_incoming_category.html', context)

@login_prohibited   
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
    
@login_prohibited
def news_page(request):
    articles = all_articles['articles']
    return render(request, 'news_page.html',{'articles':articles})   

@login_required
def add_spending_transaction(request,request_id):
    category = get_object_or_404(SpendingCategory, id=request_id)
    #category_limit = category.limit
    if request.method == 'POST':
        create_transaction_form = SpendingTransactionForm(request.POST)
        if create_transaction_form.is_valid():
            create_transaction_form.save(commit=False)
            title=create_transaction_form.cleaned_data.get('title')
            date=create_transaction_form.cleaned_data.get('date')
            amount=create_transaction_form.cleaned_data.get('amount')
            notes=create_transaction_form.cleaned_data.get('notes')
            receipt=create_transaction_form.cleaned_data.get('receipt')
            transaction=SpendingTransaction.objects.create(
                title=title,date=date,amount=amount,notes=notes,spending_category=category,receipt=receipt
            )
            transaction.save()
            category.addTransaction(transaction.amount)
            category.save()
            messages.add_message(request, messages.SUCCESS,
                             "Transaction created!")
            return HttpResponseRedirect(reverse('spending'))
    else:
        create_transaction_form = SpendingTransactionForm()   
    
    context = {
        'request_id': request_id,
        'create_transaction_form': create_transaction_form,
    }
    return render(request, 'add_spending_transaction.html', context)

@login_required
def add_income_transaction(request, request_id):
    category = get_object_or_404(IncomeCategory, id=request_id)
    if request.method == 'POST':
        create_transaction_form = IncomeTransactionForm(request.POST)
        if create_transaction_form.is_valid():
            create_transaction_form.save(commit=False)
            title=create_transaction_form.cleaned_data.get('title')
            date=create_transaction_form.cleaned_data.get('date')
            amount=create_transaction_form.cleaned_data.get('amount')
            notes=create_transaction_form.cleaned_data.get('notes')
            transaction=IncomeTransaction.objects.create(
                title=title,date=date,amount=amount,notes=notes,income_category=category
            )
            transaction.save()
            messages.add_message(request, messages.SUCCESS,
                             "Transaction created!")
            return HttpResponseRedirect(reverse('incomings'))
    else:
        create_transaction_form = IncomeTransactionForm()   
    
    context = {
        'request_id': request_id,
        'create_transaction_form': create_transaction_form,
    }
    return render(request, 'add_income_transaction.html', context)


@login_required
def list_incomings(request):
    incomings = Transaction.incomings.all()
    context = {
        'incomings': incomings,
    }
    return render(request, 'incomings.html', context=context)

def get_total_transactions_by_date(request, from_date, to_date):
    return SpendingTransaction.spendings.filter(
        date__gte=from_date,
        date__lte=to_date,
        category__user=request.user
    ).annotate(month=TruncMonth("date")).values("month").annotate(total=Sum("amount")).values("month", "total")

@login_required
def view_report(request):
    #from_date = date(date.today().year-1, date.today().month, 1)
    #to_date = date.today()

    if request.method == "POST":
        form = DateReportForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get("from_date")
            to_date = form.cleaned_data.get("to_date")
    #else:
    #    form = DateReportForm(initial={
    #        "from_date": from_date,
    #        "to_date": to_date
    #    })
    
    #transactions = get_total_transactions_by_date(request, from_date, to_date)
    else:
        form=DateReportForm()
    context = {
        "form": form,
        #"transactions": transactions,
    }
    return render(request, 'report.html', context=context)

@login_required
def view_settings(request):
    current_user = request.user
    toggle = current_user.toggle_notification
    return render(request,'settings.html',{'toggle':toggle})

@login_required
def toggle_notification(request):
    current_user = request.user
    if current_user.toggle_notification == 'ON':
        current_user.toggle_notification='OFF'
        current_user.save()
    else:
        current_user.toggle_notification='ON'
        current_user.save()
    return redirect('settings')

@login_required   
def add_friend(request):
    return render(request, 'add_friend.html')

@login_required
def leaderboard(request):
    return render(request, 'leaderboard.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def reports(request):
    return render(request, 'reports.html')
