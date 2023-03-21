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

    # message = "Thank you for signing up with us."
    # user_email=form.cleaned_data.get('email')
    # name=form.cleaned_data.get('name')
    # send_mail(
    #     subject="Welcome to Void Money Tracker",
    #     message=message,
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=[user_email],
    # )

    # html_content = render_to_string(
    #     "emails/email_template.html",
    #     {
    #         'title': 'Welcome to Void Money Tracker',
    #         'content': 'You have been successfully signed up.'
    #     })
    # text_content = strip_tags(html_content)
    # email = EmailMultiAlternatives(
    #     #subject
    #     "Welcome to Void Money Tracker",
    #     #content
    #     text_content,
    #     #from_email
    #     settings.EMAIL_HOST_USER,
    #     #recipient_list
    #     [user.email]
    # )
    # email.attach_alternative(html_content, "text/html")

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

    ''' /Can be used to personalise reset email, requires token to be made in view and saved for user in seperate model (this implementation is currently not used)/
    def send_forgot_password_email(self, to, token):
        subject = 'Your forgot password link'
        message = f'Hi, click on this link to reset your password: http://127.0.0.1:8000/password-change/{token}/'
        email_from = settings.DEFAULT_FROM_EMAIL
        to = [to]
        send_mail(subject, message, email_from, to)
        return True
    '''
