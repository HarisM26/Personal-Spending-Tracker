from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def features(request):
    return render(request, 'features.html')