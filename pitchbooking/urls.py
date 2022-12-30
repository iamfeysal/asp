from django.urls import path
from pitchbooking.views import BookingCreateWizardView, BookingHomeView, \
    BookingListView, BookingSettingsView,BookingDeleteView, BookingApproveView, \
    get_available_time

urlpatterns = [
    # path('', list_futsal_pitch, name='list_futsal'),
    # path('booking/', book_futsal, name='book_futsal'),
    path("", BookingCreateWizardView.as_view(), name="create_booking"),
    path("admins", BookingHomeView.as_view(), name="admin_dashboard"),
    path("admins/list", BookingListView.as_view(), name="booking_list"),
    path("admins/settings", BookingSettingsView.as_view(), name="booking_settings"),
    path("admins/<pk>/delete",
         BookingDeleteView.as_view(), name="booking_delete"),
    path("admins/<pk>/approve",
         BookingApproveView.as_view(), name="booking_approve"),
    path("get-available-time", get_available_time, name="get_available_time"),
]