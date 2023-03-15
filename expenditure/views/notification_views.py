from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenditure.models.notification import Notification
from expenditure.helpers import *


@login_required
def notification_page(request):
    current_user = request.user
    notifications = get_user_notifications(current_user)
    context = {
        'notifications': notifications,
    }
    return render(request, 'notification_page.html', context)


@login_required
def toggle_notification(request):
    current_user = request.user
    if current_user.toggle_notification == 'ON':
        current_user.toggle_notification = 'OFF'
        current_user.save()
    else:
        current_user.toggle_notification = 'ON'
        current_user.save()
    return redirect('settings')


@login_required
def view_selected_notification(request, id):
    notification = Notification.objects.get(id=id)
    notification.status = 'read'
    notification.save()
    context = {
        'notification': notification,
    }
    return render(request, 'view_notification.html', context)
