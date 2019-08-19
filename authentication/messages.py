import logging

from django.views import debug


from django.core.mail import send_mail
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException

LOGGER = logging.getLogger(__name__)


def send_email(subject, message, recipient_list=None, **kwargs):
    print("hit send email function")
    if not debug :
        category = 'email'
        from_email = kwargs.pop('from_email', 'iamfeysal@shopsoko.com')
        print(from_email)
        html_message = kwargs.pop('html_message', None)
        print(html_message)
        obj = kwargs.pop('obj', None)
        print(obj)
        if not isinstance(recipient_list, list) :
            recipient_list = [recipient_list]

        try:
            response = send_mail(
                subject, message, from_email, recipient_list,
                fail_silently=False, html_message=html_message, **kwargs, obj=obj
            )
            print(response)
            return response
        except BadHeaderError as err :
            LOGGER.exception(err)
