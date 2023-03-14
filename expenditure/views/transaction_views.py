from django.shortcuts import render, get_object_or_404
from expenditure.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.helpers import *
from django.contrib.auth.decorators import login_required


@login_required
def add_quick_spending(request):
    spending_catgeory_queryset = SpendingCategory.objects.filter(
        user=request.user)

    # later do .filter(name='General') or order by id and then first (if general would be deleted)
    form = QuickSpendingTransactionForm(
        initial={'spending_category': spending_catgeory_queryset.first()})

    if request.method == 'POST':
        form = QuickSpendingTransactionForm(request.POST)
        if form.is_valid():
            today = date.today()
            amount = form.cleaned_data.get('amount')
            spending_category = form.cleaned_data.get('spending_category')
            title = f'QuickTransaction {spending_category}'
            transaction = SpendingTransaction.objects.create(
                title=title,
                amount=amount,
                spending_category=spending_category,
                is_current=True,
                date=today
            )
            messages.add_message(request, messages.SUCCESS,
                                 "Transaction created!")
            form = QuickSpendingTransactionForm(
                initial={'spending_category': spending_category})

    form.fields['spending_category'].queryset = spending_catgeory_queryset

    return form


@login_required
def add_spending_transaction(request, request_id):
    category = get_object_or_404(SpendingCategory, id=request_id)
    # category_limit = category.limit
    if request.method == 'POST':
        create_transaction_form = SpendingTransactionForm(
            request.POST, request.FILES)
        if create_transaction_form.is_valid():
            create_transaction_form.save(commit=False)
            title = create_transaction_form.cleaned_data.get('title')
            date = create_transaction_form.cleaned_data.get('date')
            amount = create_transaction_form.cleaned_data.get('amount')
            notes = create_transaction_form.cleaned_data.get('notes')
            receipt = create_transaction_form.cleaned_data.get('receipt')
            transaction = SpendingTransaction.objects.create(
                title=title, date=date, amount=amount, notes=notes, spending_category=category, receipt=receipt
            )
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
            title = create_transaction_form.cleaned_data.get('title')
            date = create_transaction_form.cleaned_data.get('date')
            amount = create_transaction_form.cleaned_data.get('amount')
            notes = create_transaction_form.cleaned_data.get('notes')
            transaction = IncomeTransaction.objects.create(
                title=title, date=date, amount=amount, notes=notes, income_category=category
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
def edit_spending_transaction(request, id):
    spending_transaction = get_object_or_404(SpendingTransaction, id=id)
    amount = spending_transaction.amount

    if request.method == 'POST':
        form = SpendingTransactionForm(
            request.POST, request.FILES, instance=spending_transaction)
        if form.is_valid():
            form.save(commit=False)
            if not (amount == form.cleaned_data.get('amount')):
                spending_transaction.spending_category.limit.remaining_amount += (
                    amount - form.cleaned_data.get('amount'))
                spending_transaction.spending_category.limit.save()
            form.save()
            return HttpResponseRedirect(reverse('spending'))
    else:
        form = SpendingTransactionForm(instance=spending_transaction)

    context = {
        'spending_transaction': spending_transaction,
        'form': form,
    }
    return render(request, 'edit_spending_transaction.html', context=context)


@login_required
def edit_incoming_transaction(request, id):
    income_transaction = get_object_or_404(IncomeTransaction, id=id)

    if request.method == 'POST':
        form = IncomeTransactionForm(request.POST, instance=income_transaction)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('incomings'))
    else:
        form = IncomeTransactionForm(instance=income_transaction)

    context = {
        'income_transaction': income_transaction,
        'form': form,
    }
    return render(request, 'edit_income_transaction.html', context=context)


@login_required
def delete_spending_transaction(request, id):
    spending = get_object_or_404(SpendingTransaction, id=id)
    spending.spending_category.limit.remaining_amount += spending.amount
    spending.spending_category.limit.save()
    spending.delete()
    messages.success(request, "transaction deleted successfully!")
    return HttpResponseRedirect(reverse('spending'))


@login_required
def delete_incoming_transaction(request, id):
    income = get_object_or_404(IncomeTransaction, id=id)
    income.delete()
    return HttpResponseRedirect(reverse('incomings'))


@login_required
def view_transaction(request, id):
    transaction = get_object_or_404(SpendingTransaction, id=id)
    context = {
        'transaction': transaction,
    }

    return render(request, 'transaction.html', context=context)


@login_required
def list_incomings(request):
    incomings = IncomeTransaction.objects.all()
    context = {
        'incomings': incomings,
    }
    return render(request, 'incomings.html', context=context)
