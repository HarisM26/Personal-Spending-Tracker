from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime, timedelta
from django.conf import settings
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages
from decimal import Decimal
from expenditure.models.notification import Notification
from expenditure.models.categories import SpendingCategory
from expenditure.models.limit import Limit


"""Inspiration taken from https://groups.google.com/g/django-developers/c/LHnM_2jnZOM/m/8-oK6CXyEAAJ"""


def not_future(val):
    if val > date.today():
        raise ValidationError(_("Date should not be in the future."))
    elif not (isinstance(val, date)):
        raise ValidationError(
            _("Date should be in the right format: YYYY-MM-DD."))


def create_limit_notification(user, category_name, category_limit_obj, total):
    if total >= (category_limit_obj.calc_90_percent_of_limit) and total < Decimal(category_limit_obj.limit_amount):
        current_message = f'{category_name} category is close to its limit.\
                                            You now have £{category_limit_obj.remaining_amount} remaining to spend. \
                                            Please consider reducing your spending'
    else:
        current_message = f'{category_name} category has reached its limit!'

    notification = Notification.objects.create(
        user_receiver=user,
        title='About your limit',
        message=current_message
    )
    return notification


def create_notification_about_refresh(user, category):
    notification = Notification.objects.create(
        user_receiver=user,
        title='Yey!, A category has refreshed.',
        message=f'{category.name} category has refreshed. Let\'s not go over our £{category.limit} limit this time!. Happy saving!!'
    )
    return notification


def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function


def get_end_date(limit_type):
    if limit_type == 'daily':
        return datetime.date(datetime.now())
    elif limit_type == 'weekly':
        return datetime.date(datetime.now()) + timedelta(days=6)
    elif limit_type == 'monthly':
        return datetime.date(datetime.now()) + timedelta(days=27)
    else:
        return datetime.date(datetime.now()) + timedelta(days=364)


def create_default_categories(user):
    default_general = SpendingCategory.objects.create(
        user=user,
        name='General',
        limit=Limit.objects.create(
            limit_amount=Decimal('500'),
            start_date=date.today(),
            end_date=datetime.now() + timedelta(days=30),
            remaining_amount=Decimal('500.00'),
        )
    )
    default_groceries = SpendingCategory.objects.create(
        user=user,
        name='Groceries',
        limit=Limit.objects.create(
            limit_amount=Decimal('400.00'),
            start_date=date.today(),
            end_date=datetime.now() + timedelta(days=30),
            remaining_amount=Decimal('400.00'),
        )
    )
    default_transport = SpendingCategory.objects.create(
        user=user,
        name='Transport',
        limit=Limit.objects.create(
            limit_amount=Decimal('200.00'),
            start_date=date.today(),
            end_date=datetime.now() + timedelta(days=30),
            remaining_amount=Decimal('200.00')
        )
    )
    default_utilities = SpendingCategory.objects.create(
        user=user,
        name='Utilities',
        limit=Limit.objects.create(
            limit_amount=Decimal('100.00'),
            start_date=date.today(),
            end_date=datetime.now() + timedelta(days=30),
            remaining_amount=Decimal('100.00'),
        )
    )
    return default_general, default_groceries, default_transport, default_utilities


def sending_email(message, user):
    send_mail(
        'This is VOID Money Tracker',
        message,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )


def check_league(request):
    user = request.user
    if (user.league_status == 'bronze' and int(user.points) >= 200):
        user.league_status = 'silver'
        user.save()
        sending_email(
            'Congratulations! You have reached the Silver League. You need to have 600 points to progress to the next league.',
            user
        )
        messages.success(
            request, "Congratulations! You have reached the Silver League. You need to have 150 points to progress to the next league.")
    elif ((user.league_status == 'silver' and int(user.points) >= 600)):
        user.league_status = 'gold'
        user.save()
        sending_email(
            'Congratulations! You have reached the Gold League. You need to have 1800 points to progress to the next league.',
            user
        )
        messages.success(
            request, "Congratulations! You have reached the Gold League. You need to have 300 points to progress to the next league.")
    elif ((user.league_status == 'gold' and int(user.points) >= 1800)):
        user.league_status = 'platinum'
        user.save()
        sending_email(
            'Congratulations! You have reached the Platinum League. You need to have 5000 points to progress to the next league.',
            user
        )
        messages.success(
            request, "Congratulations! You have reached the Platinum League. You need to have 500 points to progress to the next league.")
    elif ((user.league_status == 'platinum' and int(user.points) >= 5000)):
        user.league_status = 'diamond'
        user.save()
        messages.success(
            request, "Congratulations! You have reached the final Diamond League. You will shortly recieve a present from us!")
        sending_email(
            'You have reached the final Diamond League! You can now get unlimited access to tips from our financial advisors and a chance to meet one!',
            user
        )
