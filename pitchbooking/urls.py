from django.urls import path
from pitchbooking.views import BookingCreateWizardView

urlpatterns = [
    # path('', list_futsal_pitch, name='list_futsal'),
    # path('booking/', book_futsal, name='book_futsal'),
    path("", BookingCreateWizardView.as_view(), name="create_booking"),
]