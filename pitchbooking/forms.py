from django import forms
from .models import Pitch, Booking, BookingSettings


# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['pitch', 'date', 'time', ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['pitch'].queryset = Pitch.objects.all()


class ChangeInputsStyle(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            # get current classes from Meta
            input_type = self.fields[field].widget.input_type
            classes = self.fields[field].widget.attrs.get("class")
            if classes is not None:
                classes += " form-check-input" if input_type == "checkbox" else " form-control  flatpickr-input"
            else:
                classes = " form-check-input" if input_type == "checkbox" else " form-control flatpickr-input"
            self.fields[field].widget.attrs.update({
                'class': classes
            })


class BookingDateForm(ChangeInputsStyle):
    date = forms.DateField(required=True)


class BookingTimeForm(ChangeInputsStyle):
    time = forms.TimeField(widget=forms.HiddenInput())


class BookingCustomerForm(ChangeInputsStyle):
    user_name = forms.CharField(max_length=250)
    user_email = forms.EmailField()
    user_mobile = forms.CharField(required=False, max_length=10)
