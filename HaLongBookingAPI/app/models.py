from django.db import models

# Create your models here.
class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='Unknow')
    srcImg = models.URLField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    star = models.PositiveSmallIntegerField(blank=True, default=1)
    address = models.CharField(max_length=200, blank=True, default='')
    freeServices = models.TextField()
    services = models.TextField()
    isSale = models.BooleanField(blank=True, default=False)
    numberBookings = models.IntegerField(default=0)

    class Meta:
        ordering = ['numberBookings', 'id']


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='Unknow')
    srcImg = models.URLField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    freeServices = models.TextField()
    capacity = models.TextField()
    numberBookings = models.IntegerField(default=0)
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)

    class Meta:
        ordering = ['numberBookings', 'id']

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    nameCustomer = models.CharField(max_length=100, blank=False, default='Unknow')
    phoneNumber = models.CharField(max_length=20, blank=False, default='')
    email = models.EmailField(max_length=50, blank=False)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    numberAdult = models.IntegerField(default=0)
    numberChildren = models.IntegerField(default=0)
    numberBaby = models.IntegerField(default=0)
    note = models.TextField()
    status = models.CharField(max_length=10, blank=False, default='New')
    bookingDate = models.DateField()

    class Meta:
        ordering = ['bookingDate']
