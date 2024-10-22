from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenditure.news_api import all_articles
from expenditure.helpers import *
from django.contrib.auth.decorators import login_required
from expenditure.views.transaction_views import add_quick_spending
from expenditure.views.report_views import feed_page_report


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
    check_league(request)
    form = add_quick_spending(request)
    articles = all_articles['articles']
    articles = articles[0:4]

    feed_report_context = feed_page_report(request)

    context = {
        'categories_within_limit': feed_report_context['categories_within_limit'],
        'total_budget': feed_report_context['total_budget'],
        'remaining_budget': feed_report_context['remaining_budget'],
        'total_spending': feed_report_context['total_spending'],
        'total_income': feed_report_context['total_income'],
        'income_categories': feed_report_context['income_categories'],
        'articles': articles,
        'form': form,
        'user_points': request.user.points,
        'messages': messages.get_messages(request),
    }

    return render(request, 'feed.html', context)


@login_prohibited
def features(request):
    return render(request, 'features.html')


@login_required
def view_settings(request):
    current_user = request.user
    toggle = current_user.toggle_notification
    toggle_priv = current_user.toggle_privacy
    toggle_email = current_user.toggle_email

    return render(request, 'settings.html', {'toggle': toggle, 'toggle_priv': toggle_priv, 'toggle_email': toggle_email})
