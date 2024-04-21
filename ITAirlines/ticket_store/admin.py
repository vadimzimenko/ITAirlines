from django.contrib import admin
from .models import *

class FlightInLine(admin.StackedInline):
    model = Flight

class TicketInLine(admin.StackedInline):
    model = Ticket

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ["name", "airline_code", "website"]

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    inlines = [FlightInLine]
    list_display = ["name", "tail_number", "model", "num_seats"]

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["airport_name", "airport_code", "country", "city"]

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    #inlines = [TicketInLine]
    list_display = ["flight_code", "departure_airport", "arrival_airport", "airplane", "departure_date"]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["flight", "seat_num", "bought"]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["user", "flight", "status"]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["booking", "ammount_paid", "payment_date"]