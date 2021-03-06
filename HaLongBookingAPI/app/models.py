from django.db import models
from datetime import datetime   
from django.conf import settings

# Create your models here.
class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='Unknow')
    srcImg = models.URLField(max_length=200, blank=True, default='')
    srcDetailImgs = models.TextField(blank=False, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    star = models.PositiveSmallIntegerField(blank=True, default=1)
    address = models.CharField(max_length=200, blank=True, default='')
    freeServices = models.TextField()
    services = models.TextField()
    isSale = models.BooleanField(blank=True, default=False)

    class Meta:
        ordering = ['id']


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='Unknow')
    srcImg = models.URLField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    freeServices = models.TextField()
    capacity = models.TextField()
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    nameCustomer = models.CharField(max_length=100, blank=False, default='Unknow')
    phoneNumber = models.CharField(max_length=20, blank=False, default='')
    email = models.EmailField(max_length=50, blank=False)
    checkInDate = models.DateField(default=datetime.now, blank=True)
    checkOutDate = models.DateField(default=datetime.now, blank=True)
    numberAdult = models.IntegerField(default=0)
    numberChildren = models.IntegerField(default=0)
    numberBaby = models.IntegerField(default=0)
    note = models.TextField()
    status = models.CharField(max_length=10, blank=False, default='New')
    bookingDate = models.DateTimeField(default=datetime.now, blank=True)
    hotel = models.ForeignKey(Hotel, related_name='bookings', on_delete=models.CASCADE, default=None)
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['-bookingDate']

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100, blank=False, default='')
    password = models.CharField(max_length=100, blank=False, default='')
    email = models.EmailField(max_length=50, blank=False, default='')

    class Meta:
        ordering = ['id']

class BookingTimeline(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Admin, related_name='bookingTimelines', on_delete=models.CASCADE, default=None)
    booking = models.ForeignKey(Booking, related_name='bookingTimelines', on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=20, blank=False, default='New')
    modifiedDate = models.DateTimeField(default=datetime.now, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-modifiedDate']

