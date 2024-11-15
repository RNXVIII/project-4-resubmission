from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  
    path('bookings/', views.BookingList.as_view(), name='booking_list'),  
    path('my-bookings/', views.UserBookingList.as_view(), name='user_booking'),  
    path('booking/edit/<int:pk>/', views.edit_booking, name='edit_booking'),  
    path('booking/delete/<int:pk>/', views.delete_booking, name='delete_booking'),  
]