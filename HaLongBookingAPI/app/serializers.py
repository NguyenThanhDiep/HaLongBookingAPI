from app.models import Hotel, Room, Booking, Admin, BookingTimeline
from rest_framework import serializers
   
#Manage Booking Area
class HotelBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name"]

class RoomBaseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Room
        fields = ["id", "name"]

class BookingSerializer(serializers.ModelSerializer):
    hotel = HotelBaseSerializer(read_only=True)
    room = RoomBaseSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "nameCustomer", "phoneNumber", "email", "status", "bookingDate", "hotel", "room"]

class RoomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Room
        fields = ["id", "name", "srcImg", "price", "freeServices", "capacity", "bookings"]

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name", "srcImg", "price", "star", "address", "freeServices", "services", "isSale", "bookings"]

class BookingDetailSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "nameCustomer", "phoneNumber", "email", "checkInDate", "checkOutDate", "numberAdult", "numberChildren", "numberBaby", "note", "status", "bookingDate", "hotel", "room"]

class RoomDetailSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["id", "name", "srcImg", "price", "freeServices", "capacity", "hotel", "bookings"]
        depth = 1

class HotelDetailSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ["id", "name", "srcImg", "srcDetailImgs", "price", "star", "address", "freeServices", "services", "isSale", "rooms", "bookings"]

#Admin User Area
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["id", "userName", "password", "email"]

class BookingTimelineSerializer(serializers.ModelSerializer):
    admin = AdminSerializer(read_only=True)

    class Meta:
        model = BookingTimeline
        fields = ["id", "admin", "booking", "status", "modifiedDate", "description"]
