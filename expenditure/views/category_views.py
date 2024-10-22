from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from expenditure.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from expenditure.models.categories import *
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from expenditure.helpers import *
from django.contrib.auth.decorators import login_required


@login_required
def spending(request):
    check_league(request)
    current_user = request.user
    categories = SpendingCategory.objects.filter(user=current_user)
    context = {
        'categories': categories,
        'messages': messages.get_messages(request),
    }
    return render(request, 'spending.html', context)


@login_required
def create_incoming_category(request):
    current_user = request.user
    if request.method == 'POST':
        form = IncomeCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            incoming_category = IncomeCategory.objects.create(
                user=current_user, name=name)
            messages.add_message(request, messages.SUCCESS,
                                 "Category created!")
            return redirect('create_incoming_category')
        messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
    else:
        form = IncomeCategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'create_incoming_category.html', context)


@login_required
def incoming(request):
    current_user = request.user
    categories = IncomeCategory.objects.filter(user=current_user)
    context = {
        'categories': categories,
    }
    return render(request, 'incomings.html', context)


@login_required
def DeleteSpendingCategory(request, pk):
    spending_category = get_object_or_404(SpendingCategory, id=pk)

    if request.method == 'POST':
        spending_category.delete()
        return redirect('spending')

    return render(request, 'delete_spending_category.html', {'spending_category': spending_category})


@login_required
def DeleteIncomeCategory(request, pk):
    income_category = get_object_or_404(IncomeCategory, id=pk)

    if request.method == 'POST':
        income_category.delete()
        return redirect('incomings')

    return render(request, 'delete_income_category.html', {'income_category': income_category})


# UpdateView requirements:
# model; tell Django to update model records
# form_class; current values of category are populated in form to show user
# success_url; if update is successful go back to spending page


class EditSpendingCategoryView(LoginRequiredMixin, UpdateView):
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


class CreateSpendingCategoryView(LoginRequiredMixin, CreateView):

    template_name = "create_category.html"
    form_class = CategoryCreationMultiForm

    def form_valid(self, form):
        limit = form['limit'].save(commit=False)
        limit.remaining_amount = limit.limit_amount
        limit.end_date = get_end_date(limit.time_limit_type)
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
