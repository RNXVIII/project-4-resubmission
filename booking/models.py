from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    table_number = models.IntegerField(default=1)  # learned from CI
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'table_number')

    def __str__(self):
        return f"{self.date} - Table {self.table_number} - {'Booked' if self.booked else 'Available'} by {self.user.username if self.booked else 'N/A'}"

