# Required for sending emails
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid


class EmailSender():

    WELCOME_EMAIL_TEMPLATE = 'emails/welcome_email.html'
    APPROCHING_LIMIT_TEMPLATE = 'emails/approaching_limit_email.html'
    REACHED_LIMIT_TEMPLATE = 'emails/reached_limit_email.html'
    CUSTOMER_SERVICE_REPLY_TEMPLATE = 'emails/customer_service_reply_email.html'
    NEW_LEAGUE_REACHED_TEMPLATE = 'emails/new_league_reached_email.html'

    def __init__(self):
        pass

    def send_email(self, to, subject, template_name, context):
        """
        Sends an email to the given email address.
        """
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject,
            strip_tags(text_content),
            settings.DEFAULT_FROM_EMAIL,
            to,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    def send_welcome_email(self, user):
        """
        Sends a welcome email to the given email address.
        """
        if user.toggle_email == 'OFF':
            return

        subject = "Welcome to Void Money Tracker"
        context = {
            'first_name': user.first_name,
        }
        self.send_email(
            [user.email],
            subject,
            self.WELCOME_EMAIL_TEMPLATE,
            context,
        )

    def send_approaching_limit_email(self, user, category_name, percentage_limit_used):
        if user.toggle_email == 'OFF':
            return

        subject = "Watch out! You are approaching your limit!"
        context = {
            'first_name': user.first_name,
            'category_name': category_name,
            'percentage_limit_used': percentage_limit_used,
        }
        self.send_email(
            [user.email],
            subject,
            self.APPROCHING_LIMIT_TEMPLATE,
            context,
        )

    def send_reached_limit_email(self, user, category_name):
        if user.toggle_email == 'OFF':
            return

        subject = "Watch out! You have reached your limit!"
        context = {
            'first_name': user.first_name,
            'category_name': category_name,
        }
        self.send_email(
            [user.email],
            subject,
            self.REACHED_LIMIT_TEMPLATE,
            context,
        )

    def send_league_status_change_email(self, user):
        if user.toggle_email == 'OFF':
            return

        subject = "You have changed leagues!"
        context = {
            'first_name': user.first_name,
            'league_name': user.league_status.upper(),
        }
        self.send_email(
            [user.email],
            subject,
            self.NEW_LEAGUE_REACHED_TEMPLATE,
            context,
        )

    ''' /Can be used to personalise reset email, requires token to be made in view and saved for user in seperate model (this implementation is currently not used)/
    def send_forgot_password_email(self, to, token):
        subject = 'Your forgot password link'
        message = f'Hi, click on this link to reset your password: http://127.0.0.1:8000/password-change/{token}/'
        email_from = settings.DEFAULT_FROM_EMAIL
        to = [to]
        send_mail(subject, message, email_from, to)
        return True
    '''
