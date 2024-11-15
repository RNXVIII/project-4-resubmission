from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Booking
from datetime import date


class BookingTestCase(TestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username="user1", password="testpassword1")
        self.user2 = User.objects.create_user(username="user2", password="testpassword2")

        # Create bookings for both users
        self.booking1 = Booking.objects.create(date=date.today(), table_number=1, user=self.user1, booked=True)
        self.booking2 = Booking.objects.create(date=date.today(), table_number=2, user=self.user2, booked=True)

    def test_user_can_view_their_own_bookings(self):
        # Log in as user1
        self.client.login(username="user1", password="testpassword1")
        
        # Access the bookings page for user1
        response = self.client.get(reverse("my_bookings"))

        # Check that user1's booking is shown and user2's booking is not
        self.assertContains(response, "Table 1")
        self.assertNotContains(response, "Table 2")

    def test_user_can_add_a_booking(self):
        # Log in as user1
        self.client.login(username="user1", password="testpassword1")

        # Add a new booking for user1
        response = self.client.post(reverse("add_booking"), {
            "date": date.today(),
            "table_number": 3,
            "user": self.user1.id,
            "booked": True
        })

        # Check if the new booking exists in the database
        self.assertTrue(Booking.objects.filter(date=date.today(), table_number=3, user=self.user1).exists())

    def test_user_can_edit_their_own_booking(self):
        # Log in as user1
        self.client.login(username="user1", password="testpassword1")

        # Edit user1's booking
        response = self.client.post(reverse("edit_booking", args=[self.booking1.id]), {
            "date": date.today(),
            "table_number": 4,
            "booked": True
        })

        # Reload booking and check that the table number has been updated
        self.booking1.refresh_from_db()
        self.assertEqual(self.booking1.table_number, 4)

    def test_user_can_delete_their_own_booking(self):
        # Log in as user1
        self.client.login(username="user1", password="testpassword1")

        # Delete user1's booking
        response = self.client.post(reverse("delete_booking", args=[self.booking1.id]))

        # Check that the booking was deleted
        self.assertFalse(Booking.objects.filter(id=self.booking1.id).exists())
