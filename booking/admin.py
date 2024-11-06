from django.contrib import admin
from .models import Booking
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

@admin.register(Booking)
class BookingAdmin(SummernoteModelAdmin):
    list_display = ('id', 'date', 'table_number', 'user', 'booked')
    search_fields = ['user__username']
    list_filter = ('booked',)
