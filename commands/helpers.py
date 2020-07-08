import re
from commands.messages import send_email
from commands.repositories import new_reset_request_for_user_with_email
from users.models import User


def send_email_for_password_reset(request, email):
    """Takes care of user password ressetting"""
    # noinspection PyUnresolvedReferences
    try:
        password_reset_request = new_reset_request_for_user_with_email(email)
    except User.DoesNotExist:
        # raise alarms
        send_email(
            'Password Reset: Red Flag',
            ("An attempt to reset a password has been initiated "
             "for the email %s which does not exist on our system.")
            % (email),
            [email],
            from_email='iamfeysal@gmail.com',
            fail_silently=False,
        )
        return False

    # build base url based on domain

    base_url = request.build_absolute_uri()

    # send the email
    url = base_url + "confirm/?token=" + password_reset_request.token
    message = ("You‘ve requested to reset your ASP password "
               "with the email <b> %s</b>.<br /> If you didn't request this, "
               "you can ignore this email. %s") % (email, url)

    send_email(
        'Password Reset:ASP',
        '',
        [email],
        from_email='iamfeysal@gmail.com',
        html_message=message,
        fail_silently=False,
    )

    return True


def validate_string(password_string):
    """
    Performs a number of checks to see
    if a string can be a valid password
    """
    if len(password_string) < 8:
        message = "Password must contain atleat 8 characters."
        return (message, False)
    elif re.search('[0-9]', password_string) is None:
        message = "Password must contain atleast one number"
        return (message, False)
    else:
        message = None
        return (message, True)
