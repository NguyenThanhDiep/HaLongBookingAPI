from app.models import Hotel, Room, Booking
from app.serializers import HotelBaseSerializer, HotelSerializer, HotelDetailSerializer, RoomBaseSerializer, RoomSerializer, RoomDetailSerializer, BookingSerializer, BookingDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count

# Create your views here.
class HotelView(APIView):
    def get(self, request, format=None):
        hotels = Hotel.objects.all()
        searchString = self.request.query_params.get('searchString', None)
        if searchString is not None: 
            hotels = hotels.filter(name__contains=searchString)
        hotels = hotels.annotate(numberBookings=Count('bookings')).order_by('-numberBookings')
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HotelDetailView(APIView):
    def get_object(self, pk):
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        hotel = self.get_object(id)
        serializer = HotelDetailSerializer(instance=hotel)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        hotel = self.get_object(id)
        serializer = HotelDetailSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        hotel = self.get_object(id)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomView(APIView):
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        #serializer = RoomSerializer(data=request.data)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            model = request.data
            hotel = Hotel.objects.get(pk=model['hotelId'])
            newRoom = Room.objects.create(name=model['name'], srcImg=model['srcImg'], price=model['price'], freeServices=model['freeServices'], capacity=model['capacity'], hotel=hotel)
            serializer = RoomSerializer(newRoom)
            return Response(serializer.data)
        except Exception:
            raise Http404

class RoomDetailView(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        try:
            room = self.get_object(id)
            serializer = RoomDetailSerializer(room)
            return Response(serializer.data)
        except Room.DoesNotExist:
            raise Http404

    #def getByHotelId(self, request, id, format=None):
    #    rooms = Room.objects.filter(hotel=id)
    #    serializer = RoomSerializer(rooms, many=True)
    #    return Response(serializer.data)

    def put(self, request, id, format=None):
        room = self.get_object(id)
        serializer = RoomDetailSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        room = self.get_object(id)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingView(APIView):
    def get(self, request, format=None):
        bookings = Booking.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None: 
            bookings = bookings.filter(status=status)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            model = request.data
            hotel = Hotel.objects.get(pk=model['hotelId'])
            room = Room.objects.get(pk=model['roomId'])
            newBooking = Booking.objects.create(nameCustomer=model['nameCustomer'], phoneNumber=model['phoneNumber'], 
                                                email=model['email'], checkInDate=model['checkInDate'], checkOutDate=model['checkOutDate'], 
                                                numberAdult=model['numberAdult'], numberChildren=model['numberChildren'], numberBaby=model['numberBaby'], 
                                                note=model['note'], status='New', hotel=hotel, room=room)
            serializer = BookingSerializer(newBooking)
            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(APIView):
    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        booking = self.get_object(id)
        serializer = BookingDetailSerializer(instance=booking)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        booking = self.get_object(id)
        serializer = BookingDetailSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        booking = self.get_object(id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
