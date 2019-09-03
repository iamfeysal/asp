from django import forms

from users.models import UserFeedback


class UserFeedbackForm(forms.ModelForm) :
    class Meta :
        model = UserFeedback
        fields = ['message', 'message_polarity']

    def clean(self) :
        form_data = self.cleaned_data
        if form_data['message'] == "":
            self._errors['message'] = self.error_class(
                ["Cannot submit a blank message"])

        return form_data

    def __init__(self, *args, **kwargs) :
        super(UserFeedbackForm, self).__init__(*args, **kwargs)

        self.fields['message'].widget = forms.Textarea(
            attrs={'placeholder' : 'Enter Your Message Here.'})
