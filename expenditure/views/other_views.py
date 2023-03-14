from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenditure.news_api import all_articles
from expenditure.helpers import *
from django.contrib.auth.decorators import login_required
from expenditure.views.transaction_views import add_quick_spending


@login_prohibited
def home(request):
    articles = all_articles['articles']
    articles = articles[0:20]
    context = {
        'articles': articles,
    }
    return render(request, 'home.html', context)


@login_required
def feed(request):
    form = add_quick_spending(request)

    current_user = request.user
    unread_status_count = get_unread_nofications(current_user)
    notifications = get_user_notifications(current_user)
    articles = all_articles['articles']
    articles = articles[0:4]

    latest_notifications = notifications[0:3]
    context = {
        'latest_notifications': latest_notifications,
        'unread_status_count': unread_status_count,
        'articles': articles,
        'form': form,
    }

    return render(request, 'feed.html', context)


@login_prohibited
def about(request):
    return render(request, 'about.html')


@login_prohibited
def features(request):
    return render(request, 'features.html')


@login_prohibited
def contact(request):
    return render(request, 'contact.html')


@login_prohibited
def news_page(request):
    articles = all_articles['articles']
    return render(request, 'news_page.html', {'articles': articles})


@login_required
def view_settings(request):
    current_user = request.user
    toggle = current_user.toggle_notification
    return render(request, 'settings.html', {'toggle': toggle})
