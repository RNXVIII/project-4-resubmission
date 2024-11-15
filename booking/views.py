from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import BookingForm
from .models import Booking

# Keep the all-bookings view as it is
class BookingList(ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'

# New view for logged-in user's bookings (profile within `booking`)
class UserBookingList(ListView):
    model = Booking
    template_name = 'booking/user_booking.html'  # Separate template for user bookings
    context_object_name = 'bookings'

    def get_queryset(self):
        """Show only the bookings for the logged-in user."""
        return Booking.objects.filter(user=self.request.user)

# View for creating a booking
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

# View for editing a booking
@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully.')
            return redirect('user_booking')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/edit_booking.html', {'form': form})

# View for deleting a booking
@login_required
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
        return redirect('user_booking')
    return render(request, 'booking/delete_booking.html', {'booking': booking})