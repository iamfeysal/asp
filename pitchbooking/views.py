from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking


def book_futsal(request):
    bookings = Booking.objects.all()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_futsal')
    else:
        form = BookingForm()
    return render(request, 'booking/book_futsal.html', {'bookings': bookings, 'form': form})
