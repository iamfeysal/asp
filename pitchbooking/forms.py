from django import forms
from .models import Pitch, Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pitch', 'date', 'time', 'user_name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pitch'].queryset = Pitch.objects.all()
