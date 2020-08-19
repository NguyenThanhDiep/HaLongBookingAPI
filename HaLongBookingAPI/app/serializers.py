from app.models import Hotel, Room
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Room
        fields = ["id", "name", "srcImg", "price", "freeServices", "capacity"]

class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name", "srcImg", "price", "freeServices", "capacity", "hotel"]
        depth = 1
        
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name", "srcImg", "price", "star", "address", "freeServices", "services", "isSale"]

class HotelDetailSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ["id", "name", "srcImg", "price", "star", "address", "freeServices", "services", "isSale", "rooms"]
