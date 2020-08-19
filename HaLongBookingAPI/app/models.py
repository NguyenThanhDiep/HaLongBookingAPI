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
