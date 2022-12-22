from django.contrib import admin

# Register your models here.
from pitchbooking.models import Pitch, Booking, BookingSettings

admin.site.register(Pitch)
admin.site.register(Booking)
admin.site.register(BookingSettings)
