from django.db import models
from django.utils import timezone

from django_countries.fields import CountryField
from accounts.models import CustomUser

class Airline(models.Model):
    '''Модель, яка створює уявлення Авіакомпанії в БД.'''
    airline_code = models.CharField(
        max_length = 6,
        blank = False,
        help_text = "Код для авіакомпанії"
    )   

    name = models.CharField(
        max_length = 100,
        blank = False,
        help_text = "Повна назва авіакомпанії"
    )

    website = models.URLField(
        max_length = 200,
        blank = False,
        help_text = "Посилання на домашній сайт"
    )

    class Meta:
        ordering = ["-name"]
    
    def __str__(self):
        return self.name

class Airplane(models.Model):
    '''Модель, яка створює уявлення Літака в БД.'''
    name = models.CharField(
        max_length = 100,
        blank = False,
        help_text = "Назва літака",
    )
    model = models.CharField(
        max_length = 100,
        blank = False,
        help_text = "Модель літака",
    )
    tail_number = models.CharField(
        max_length = 24,
        blank = False,
        unique = True,
        help_text = "Реєстраційний номер літака",
    )
    num_seats = models.IntegerField(
        blank = False,
        help_text = "Кількість місць в літаку",
    )
    airline = models.ForeignKey(
        Airline,
        on_delete = models.CASCADE,
        blank = False,
        help_text = "Якій авіакомпанії компанії належить"
    )

    class Meta:
        ordering = ["-name",]

    def __str__(self):
        return f"{self.name}-{self.model}"

class Airport(models.Model):
    '''Модель, яка створює уявлення Аеропорту в БД. '''
    airport_code = models.CharField( 
        max_length=50,
        blank = False,
        help_text = "Код аеропорту"
    )

    airport_name = models.CharField( 
        max_length=100,
        blank = False,
        help_text = "Повна назва аеропорту"
    )

    city = models.CharField( 
        max_length=50,
        blank = False,
        help_text = "Місто знаходження аеропорту"
    )

    country = CountryField(
        blank = False,
        help_text = "Країна якій належить даний аеропорт",
    )

    class Meta:
        ordering = ["-airport_name"]

    def __str__(self):
        return self.airport_name

class Flight(models.Model):
    '''Модель, яка створює уявлення Рейсу в БД.'''
    flight_code = models.CharField(
        max_length = 8,
        blank = False,
        help_text = "Код рейсу"
    )

    departure_airport = models.ForeignKey(
        Airport,
        on_delete = models.CASCADE,
        blank = False,
        help_text = "Аеропорт, з якого відправляються",
        related_name = "departure_airport"
    )

    arrival_airport = models.ForeignKey(
        Airport,
        on_delete = models.CASCADE,
        blank = False,
        help_text = "Аеропорт, в який прибувають",
        related_name = "arrival_airport"
    )

    departure_date = models.DateTimeField(
        blank = False,
        help_text = "Дата та час відправлення",
    )

    arrival_date = models.DateTimeField(
        blank = False,
        help_text = "Дата та час прибуття"
    )

    airplane = models.ForeignKey(
        Airplane,
        on_delete = models.CASCADE,
        blank = False,
        help_text = "Який літак буде здійснювати рейс",
    )

    ticket_price = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        blank = False,
        help_text = "Вартість квитка для цього рейсу",
    )

    class Meta:
        ordering = ["-departure_date"]

    def __str__(self):
        return f"{self.flight_code}"
    
    def get_airline(self):
        return self.airplane.airline_id.name
    
    def get_flight_path(self):
        return f"{self.departure_airport.country.code},{self.departure_airport.city} ➜ {self.arrival_airport.country.code},{self.arrival_airport.city}"
    
    def get_departure_time(self):
        return timezone.localtime(self.departure_date).time()
    
    def get_arrival_time(self):
        return timezone.localtime(self.arrival_date).time()
    
    def free_seats_ammount(self):
        return len(self.ticket_set.all().filter(bought=False))

class Ticket(models.Model):
    '''Модель, яка створює уявлення Квитка в БД.'''

    flight = models.ForeignKey(
        Flight,
        on_delete = models.CASCADE,
        blank = False,
        help_text = "Рейс, на якому можна використати даний квиток",
    )

    seat_num = models.IntegerField(
        blank = False,
        help_text = "Місце в літаку",
    )

    bought = models.BooleanField(
        default = False,
        help_text = "Чи був квиток вже куплений",
    )

    def __str__(self):
        return f"Місце {self.seat_num} на рейс {self.flight}"

class Booking(models.Model):
    '''Модель, яка створює уявлення Бронювання в БД. '''
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        null = True,
        default = None,
        blank = True,
        help_text = "Хто купив даний квиток",
    )

    flight = models.ForeignKey(
        Flight,
        on_delete = models.CASCADE,
        blank = False,
        help_text = "На який рейс бронювання квитку"
    )

    ticket = models.OneToOneField(
        Ticket,
        on_delete = models.CASCADE,
        help_text = "Який саме квиток"
    )

    status_states = (
        ("PEND", "pending"),
        ("CONF", "confirmed"),
        ("CANC", "canceled"),
    )

    status = models.CharField(
        max_length = 4,
        choices = status_states,
        blank = False,
        help_text = "Статус оплати бронювання",
        default = "PEND"
    )

    def __str__(self):
        return f"Booking to flight {self.flight.flight_code} for {self.user.username}"

class Payment(models.Model):
    '''Модель, яка створює уявлення Оплати квитка в БД. '''
    booking = models.OneToOneField(
        Booking,
        on_delete = models.SET_NULL,
        blank = False,
        help_text = "З яким бронюванням пов'язано",
        null = True
    )

    payment_date = models.DateTimeField(
        blank = False,
        help_text = "Дата та час транзакції",
        auto_now_add = True
    )

    ammount_paid = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        blank = False,
        help_text = "Сплачена сума за бронювання",
    )

    def __str__(self):
        return f"{self.id}"