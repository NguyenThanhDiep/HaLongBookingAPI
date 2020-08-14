from app.models import Hotel, Room
from rest_framework import serializers

class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = ("id", "name", "srcImg", "price", "star", "address", "freeServices", "services", "isSale")


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)

    class Meta: 
        model = Room
        fields = ("id", "name", "srcImg", "price", "freeServices", "capacity", "hotel")

