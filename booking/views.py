from django.shortcuts import render
from django.views import generic
from .models import Booking
# Create your views here.

class BookingList(generic.ListView):
    queryset = Booking.objects.all()
    template_name = "booking_list.html"
    context_object_name = "bookings"  # using {% for booking in bookings %} instead of {% for booking in object_list %}.