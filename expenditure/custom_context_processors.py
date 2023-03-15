from expenditure.models.notification import Notification


def get_notification(request):
    current_user = request.user
    unread_status_count = Notification.objects.filter(
        user_receiver=current_user, status='unread').count()
    latest_notifications = Notification.objects.filter(
        user_receiver=current_user)[0:3]
    context = {
        'latest_notifications': latest_notifications,
        'unread_status_count': unread_status_count,
    }
    return context
