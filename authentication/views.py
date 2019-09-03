from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import UserCreationForm
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import PasswordResetRequest
from commands.helpers import send_email_for_password_reset
from commands.repositories import find_active_password_request, reset_password

class HomePageView(TemplateView) :
    template_name = 'home.html'


color_list = [
            'rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)', 'rgb(54, 162, 235)',
            'rgb(153, 102, 255)', 'rgb(201, 203, 207)', '#f44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5',
            '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107',
            '#FF9800', '#FF5722', '#795548', '#9E9E9E', '#607D8B', '#b71c1c', '#880E4F', '#4A148C', '#311B92',
            '#1A237E', '#0D47A1', '#01579B', '#006064', '#004D40', '#1B5E20', '#33691E', '#827717', '#F57F17',
            '#FF6F00', '#E65100', '#BF360C', '#3E2723', '#212121', '#263238'
        ]

def SignUp(request) :
    print('hit function')
    if request.method == 'POST':
        print('hit post function')
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            print(email)
            raw_password = form.cleaned_data.get('password1')
            print(raw_password)
            authentication = authenticate(email=email, password=raw_password)
            print(authentication)
            login(request, authentication)
            return redirect('home')
        else:
            messages.error(request, "Error")
            form = UserCreationForm()
    else :
        form = UserCreationForm()
    return render(request, 'registration/signup.html',{'form' : form})


def login_view(request) :
    user = request.user
    if user.is_authenticated :
        return redirect("home")

    if request.POST :
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid() :
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user :
                login(request, user)
                return redirect("home")
        else: # get form
            form=AccountAuthenticationForm()
    else :
        form = AccountAuthenticationForm()
    # print(form)
    return render(request, "registration/login.html", {'form' : form})


def logout_request(request) :
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")



def password_reset(request):
    """
    Issues a request to reset password using 'email'
    """
    err_message = None
    success_message = None

    if request.method == 'POST':
        email = request.POST['email']
        try:
            validate_email(email)
        except ValidationError:
            # return with error
            err_message = "Invalid details provided!"
        else:
            send_email_for_password_reset(email, request)
            success_message = ("An email was sent to %s "
                               "with futher instructions.") % (email)

    context = {
        'title': 'Password Reset',
        'err_message': err_message,
        'success_message': success_message,
    }

    return render(request, 'password_reset.html', context)


def password_reset_confirm(request):
    """ Confirms or rejects password reset requests """
    token = False
    if 'token' in request.GET:
        token = request.GET['token']

        # check if we have the token is storage
        try:
            find_active_password_request(token)
        except PasswordResetRequest.DoesNotExist:
            raise Http404

    # process new passwords submitted
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        token = request.POST['token']

        # TODO: add validation based on password length and other required
        # characters
        if password1 == password2:
            try:
                reset_password(token, password1)
                return HttpResponseRedirect('/')
            except Exception as exception:
                raise Exception(str(exception))
    context = {
        'title': 'Password Reset',
        'token': token,
    }

    return render(request, 'password_confirmation.html', context)