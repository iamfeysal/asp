# from django import forms
# from django.forms import ModelForm, Textarea, TextInput, Select
# from django.contrib.admin import widgets
# from django.contrib.admin.widgets import FilteredSelectMultiple
# from django.contrib.admin import widgets
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.utils.translation import ugettext_lazy as _, get_language
# from authentication.models import User
#
#
# class UserAddForm(forms.ModelForm):
#     """A form for creating new users.
#
#     Includes all the required fields, plus a repeated password.
#     """
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(
#         label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('email', 'is_player', 'is_coach')
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserAddForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     """A form for updating users.
#
#     Includes all the fields on the user,
#     but replaces the password field with admin's password hash display field.
#     """
#     password = ReadOnlyPasswordHashField(label=_("Password"),
#                                          help_text=_("Raw passwords are not stored, so there is no way to see "
#                                                      "this user's password, but you can change the password "
#                                                      "using <a href=\"password/\">this form</a>."))
#
#     class Meta:
#         model = User
#         fields = ('email', 'is_player', 'is_coach')
#
#     def clean_password(self):
#         return self.initial["password"]


from django import forms
from django.contrib.auth import forms as auth_forms
from authentication.models import User


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>.")




    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]



































