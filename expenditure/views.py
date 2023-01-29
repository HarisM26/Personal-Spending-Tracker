from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .models import Transaction
from .forms import TransactionForm

# Create your views here.


def home(request):
    return render(request, 'index.html')

def addTransaction(request):
    if request.method == 'POST':
        create_transaction_form = TransactionForm(request.POST, request.FILES)
        if create_transaction_form.is_valid():
            if request.FILES:
                file = request.FILES['reciept']
                fs = FileSystemStorage()
                file_name = fs.save(file.name, file)
                file_url = fs.url(file_name)
                print(file_name, file_url)
                create_transaction_form.cleaned_data['reciept'] = file_url
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