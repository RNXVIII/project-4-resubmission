from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import BookingForm
from .models import Booking

# Function-based view to handle booking creation
@login_required
def index(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            table_number = form.cleaned_data['table_number']
            user = request.user

            # Check if the table is already booked for the selected date
            existing_booking = Booking.objects.filter(date=date, table_number=table_number).exists()

            if existing_booking:
                messages.error(request, 'This table is already booked for the selected date.')
            else:
                booking = form.save(commit=False)
                booking.user = user
                booking.booked = True  
                booking.save()
                messages.success(request, 'Booking successfully created.')
                return redirect('home')  
        else:
            messages.error(request, 'There was an error with your booking.')
    else:
        form = BookingForm()

    context = {
        'form': form,
    }
    return render(request, 'booking/index.html', context)


class BookingList(ListView):
    model = Booking
    template_name = 'booking/booking_list.html'  
    context_object_name = 'bookings'  # allows you to use {booking in bookings} rather than booking in {booking in object_list}
