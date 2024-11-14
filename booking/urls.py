
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  
    path('bookings/', views.BookingList.as_view(), name='booking_list'),  
]
