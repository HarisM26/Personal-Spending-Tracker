# Required for sending emails
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailSender():

    WELCOME_EMAIL_TEMPLATE = 'email/welcome_email.html'

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
        content = render_to_string(template_name, context)
        send_mail(
            subject, 
            strip_tags(content),
            settings.DEFAULT_FROM_EMAIL, 
            to,
            )
    
    def send_welcome_email(self, to):
        """
        Sends a welcome email to the given email address.
        """
        context = {
            'username': to,
            'Title': 'Welcome',
        }
        self.send_email(
            to,
            'Welcome!',
            self.WELCOME_EMAIL_TEMPLATE,
            context,
        )

