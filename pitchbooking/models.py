from django.conf import settings
from django.db import models

BOOKING_PERIOD = (
    ("5", "5M"),
    ("10", "10M"),
    ("15", "15M"),
    ("20", "20M"),
    ("25", "25M"),
    ("30", "30M"),
    ("35", "35M"),
    ("40", "40M"),
    ("45", "45M"),
    ("60", "1H"),
    ("75", "1H 15M"),
    ("90", "1H 30M"),
    ("105", "1H 45M"),
    ("120", "2H"),
    ("150", "2H 30M"),
    ("180", "3H"),
)


class Pitch(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.time or "(No Name)"


class BookingSettings(models.Model):
    # General
    booking_enable = models.BooleanField(default=True)
    confirmation_required = models.BooleanField(default=True)
    # Date
    disable_weekend = models.BooleanField(default=True)
    available_booking_months = models.IntegerField(default=1,
                                                   help_text="if 2, user can only book booking for next two months.")
    max_booking_per_day = models.IntegerField(null=True, blank=True)
    # Time
    start_time = models.TimeField()
    end_time = models.TimeField()
    period_of_each_booking = models.CharField(max_length=3, default="30",
                                              choices=BOOKING_PERIOD,
                                              help_text="How long each booking take.")
    max_booking_per_time = models.IntegerField(default=1,
                                               help_text="how much booking can be book for each time.")
