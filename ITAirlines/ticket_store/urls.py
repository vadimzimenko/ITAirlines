from django.urls import path
from ticket_store import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.HomeView.as_view(), name="homepage"),
    path("airlines/", views.AirlineListView.as_view(), name="airlines"),
    path("airports/", views.AirportListView.as_view(), name="airports"),
    path("book_ticket/<int:pk>", login_required(views.TicketBookView.as_view()), name="buy_ticket_form"),
    path("cancel_booking/<int:pk>", views.BookingUpdateView.as_view(), name="cancel_booking"),
    path("flights/", views.FlightListView.as_view(), name="flights"),
    path("flights_refresh/", views.flights_refresh, name="refresh_flights_list"),
    path("flight/<int:pk>", views.FlightDetailView.as_view(), name="flight_detail"),
    path("payment/<int:booking_id>", login_required(views.PaymentCreateView.as_view()), name="payment_confirm"),
    path("payment_detail/<int:pk>", login_required(views.PaymentDetailView.as_view()), name="payment_detail"),
]