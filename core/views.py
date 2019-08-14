from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView

from asp import settings
from core.forms import SignUpForm
from core.tokens import account_activation_token

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from core.forms import SignUpForm

class HomeView(ListView) :
    model = User
    paginate_by = 10
    template_name = "home.html"


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html',)


def signup(request) :
    print("hit function")
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            print(current_site)
            subject = 'Activate Your MySite Account'
            print(subject)
            sender_email = form.cleaned_data['email']
            from_email = settings.EMAIL_HOST_USER
            print(from_email)
            to_email = [sender_email]
            print(to_email)
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # print(message)
            send_mail(
                    subject,
                    message,
                    from_email,
                    to_email,
                    fail_silently=False,
            )
            # user.email_user(subject, message, sender_email)
            print(send_mail)

            return redirect('account_activation_sent')
    else :
        form = SignUpForm()
    return render(request, 'signup.html', {'form' : form})


def activate(request, uidb64, token) :
    try :
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) :
        user = None

    if user is not None and account_activation_token.check_token(user, token) :
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else :
        return render(request, 'account_activation_invalid.html')
