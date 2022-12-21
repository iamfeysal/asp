from django.urls import path
from pitchbooking.views import book_futsal

urlpatterns = [
    path('', book_futsal, name='book_futsal'),
]