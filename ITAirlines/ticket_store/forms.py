from django import forms

from .models import Ticket, Booking, Payment

class TicketBuyForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        flight_pk = kwargs.pop('flight')
        super(TicketBuyForm, self).__init__(*args, **kwargs)
        self.fields["seat_num"] = forms.ModelChoiceField(queryset=Ticket.objects.filter(flight=flight_pk, bought=False))

    class Meta:
        fields=["seat_num"]

class BookingCancelationForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput(), initial="CANC")

    class Meta:
        model = Booking
        fields=["status"]

class PaymentCreationForm(forms.ModelForm):
    booking = forms.IntegerField(widget=forms.HiddenInput())
    ammount_paid = forms.DecimalField(widget=forms.HiddenInput())

    class Meta:
        model = Payment
        fields = ["booking", "ammount_paid"]