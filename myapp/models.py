from django.db import models
from django.utils import timezone

# Create your models here.
class Flights(models.Model):
    def __str__(self):
        return str(self.flightNo)

    fromAirport = models.CharField(max_length=4)
    toAirport = models.CharField(max_length=4)
    leavingDate = models.DateTimeField(default=timezone.now())
    arrivalDate = models.DateTimeField(default=timezone.now())
    flightNo = models.IntegerField(default=0)
    planeType = models.CharField(max_length=20, default="Plane")
    remainingSeats = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    stopOvers = models.CharField(max_length=20, default="0")

    class Meta:
        db_table = "Flights"

class Customers(models.Model):
    def __str__(self):
        return self.firstName + " " + self.lastName + " Booking No: " + str(self.bookingNo)

    flightNo = models.ForeignKey(Flights, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    bookingNo = models.IntegerField(default=0)

    class Meta:
        db_table = "Customers"
