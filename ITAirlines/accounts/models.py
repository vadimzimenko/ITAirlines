from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username
    
    def get_all_bookings(self):
        return self.booking_set.all()
    
    def get_all_available_bookings(self):
        return self.booking_set.filter(flight__departure_date__gt=timezone.now()).exclude(status='CANC')
    
    def get_all_payments(self):
        payments = []
        bookings = self.get_all_bookings()
        for booking in bookings:
            try:
                payments.append(booking.payment)
            except Exception as e:
                pass
        return payments