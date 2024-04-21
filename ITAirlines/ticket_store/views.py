from typing import Any
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, FormView, CreateView

from .models import *
from .forms import *

class HomeView(TemplateView):
    template_name = "ticket_store/index.html"
    extra_context = {
        "title": "Homepage",
        "time_now": timezone.now(),
        "today_flights": Flight.objects.filter(
            departure_date__day=timezone.now().day, 
            departure_date__month=timezone.now().month, 
            departure_date__year=timezone.now().year
            ).order_by("departure_date"),
    }

class FlightListView(ListView):
    model = Flight
    context_object_name = "flights"
    extra_context = {
        "title": "Список рейсів",
    }

class FlightDetailView(DetailView):
    model = Flight
    context_object_name = "flight"
    extra_context = {
        "time_now": timezone.now(),
    }

class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingCancelationForm
    initial = {
        'status': 'CANC'
    }
    template_name = "ticket_store/booking_update.html"
    success_url = "/accounts/personal_page" 

# HTMX views
@require_http_methods(["GET"])
def flights_refresh(request):
    context = {
        "time_now": timezone.now(),
        "today_flights": Flight.objects.filter(
            departure_date__day=timezone.now().day, 
            departure_date__month=timezone.now().month, 
            departure_date__year=timezone.now().year
            ).order_by("departure_date"),
    }
    return render(request, "ticket_store/partials/today_flights_list.html", context)

class TicketBookView(FormView):
    template_name = "ticket_store/partials/ticket_form.html"
    form_class = TicketBuyForm
    success_url = "/accounts/personal_page"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(TicketBookView, self).get_context_data(**kwargs)
        context.update({"flight_pk": self.kwargs['pk']})
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super(TicketBookView, self).get_form_kwargs()
        kwargs['flight'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        this_ticket = Ticket.objects.filter(pk=form.data['seat_num'])
        booking = Booking(
            user = self.request.user, 
            flight = this_ticket[0].flight, 
            ticket = this_ticket[0])
        this_ticket.update(bought=True)
        booking.save()
        return super().form_valid(form)
    
class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentCreationForm
    template_name = "ticket_store/payment_create.html"
    success_url = "/accounts/personal_page"

    def get_initial(self):
        booking = Booking.objects.get(pk=self.kwargs['booking_id'])
        initial = {
            "booking": booking.pk,
            "ammount_paid": booking.flight.ticket_price
        }
        return initial

class PaymentDetailView(UserPassesTestMixin, DetailView):
    model = Payment
    context_object_name = "payment"

    def test_func(self):
        return self.get_object() in self.request.user.get_all_payments()
    
class AirlineListView(ListView):
    model = Airline
    context_object_name = "airlines"

class AirportListView(ListView):
    model = Airport
    context_object_name = "airports"
