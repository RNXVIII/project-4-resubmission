from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    table_number = forms.IntegerField(label='Table Number')  

    class Meta:
        model = Booking
        fields = ['date', 'table_number']  

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        table_number = cleaned_data.get('table_number')

        if Booking.objects.filter(date=date, table_number=table_number, booked=True).exists():
            raise forms.ValidationError("This table is already booked for the selected date.")

        return cleaned_data