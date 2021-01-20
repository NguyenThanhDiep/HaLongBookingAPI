from app.models import Hotel, Room, Booking
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Room
        fields = ["id", "name", "srcImg", "price", "freeServices", "capacity", "numberBookings"]

class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name", "srcImg", "price", "freeServices", "capacity", "numberBookings", "hotel"]
        depth = 1
        
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name", "srcImg", "price", "star", "address", "freeServices", "services", "isSale", "numberBookings"]

class HotelDetailSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ["id", "name", "srcImg", "price", "star", "address", "freeServices", "services", "isSale", "numberBookings", "rooms"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "nameCustomer", "phoneNumber", "email", "status", "bookingDate"]

class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "nameCustomer", "phoneNumber", "email", "checkInDate", "checkOutDate", "numberAdult", "numberChildren", "numberBaby", "note", "status", "bookingDate"]
