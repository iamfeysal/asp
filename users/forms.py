from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User


class RegistrationForm(UserCreationForm) :
    email = forms.EmailField(max_length=254,
                             help_text='Required. Add a valid email address.')

    class Meta :
        model = User
        fields = ('email', 'username', 'password1', 'password2',)


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta :
        model = User
        fields = ('email', 'password')

    def clean(self) :
        if self.is_valid() :
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password) :
                raise forms.ValidationError("Invalid login")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Log In'))
    #
    # def __init__(self, *args, **kwargs) :
    #     super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-lg-2'
    #     self.helper.field_class = 'col-lg-8'
    #     self.helper.layout = Layout(
    #         'email',
    #         'password',
    #         StrictButton('Sign in', css_class='btn-default'),
    #
    #     )


class AccountUpdateForm(forms.ModelForm) :
    class Meta :
        model = User
        fields = ('email', 'username',)

    def clean_email(self) :
        email = self.cleaned_data['email']
        try :
            account = User.objects.exclude(pk=self.instance.pk).get(
                email=email)
        except User.DoesNotExist :
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self) :
        username = self.cleaned_data['username']
        try :
            account = User.objects.exclude(pk=self.instance.pk).get(
                username=username)
        except User.DoesNotExist :
            return username
        raise forms.ValidationError(
            'Username "%s" is already in use.' % username)