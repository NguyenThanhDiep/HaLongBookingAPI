from app.models import Hotel, Room, Booking, Admin, BookingTimeline
from app.serializers import HotelBaseSerializer, HotelSerializer, HotelDetailSerializer, RoomBaseSerializer, RoomSerializer, RoomDetailSerializer, BookingSerializer, BookingDetailSerializer, AdminSerializer, BookingTimelineSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count

# Manage Booking Views
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
            #Add to timeline
            BookingTimeline.objects.create(admin=Admin.objects.get(pk=1), booking=newBooking, status='New')
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
        adminId = self.request.query_params.get('adminId', None)
        if serializer.is_valid():
            serializer.save()
            if adminId is not None:
                #Add to timeline
                newBooking = self.get_object(id)
                BookingTimeline.objects.create(admin=Admin.objects.get(pk=adminId), booking=newBooking, status=request.data['status'], description=request.data['description'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        booking = self.get_object(id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Admin User Views
class AdminView(APIView):
    def get(self, request, format=None):
        admins = Admin.objects.all()
        userName = self.request.query_params.get('userName', None)
        password = self.request.query_params.get('password', None)
        if userName is not None and password is not None: 
            admins = admins.filter(userName=userName, password=password)
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDetailView(APIView):
    def get_object(self, pk):
        try:
            return Admin.objects.get(pk=pk)
        except Admin.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        try:
            admin = self.get_object(id)
            serializer = AdminSerializer(admin)
            return Response(serializer.data)
        except Admin.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        admin = self.get_object(id)
        serializer = AdminSerializer(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        admin = self.get_object(id)
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingTimelineView(APIView):
    def get(self, request, format=None):
        bookingId = self.request.query_params.get('bookingId', None)
        if bookingId is not None:
            timeLines = BookingTimeline.objects.filter(booking=bookingId).order_by('modifiedDate')
            serializer = BookingTimelineSerializer(timeLines, many=True)
            return Response(serializer.data)
        bookingTimelines = BookingTimeline.objects.all()
        serializer = BookingTimelineSerializer(bookingTimelines, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            model = request.data
            admin = Admin.objects.get(pk=model['adminId'])
            booking = Booking.objects.get(pk=model['bookingId'])
            newBookingTimeline = BookingTimeline.objects.create(admin=admin, booking=booking, status=model['status'], description=model['description'])
            serializer = BookingTimelineSerializer(newBookingTimeline)
            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BookingTimelineDetailView(APIView):
    def get_object(self, pk):
        try:
            return BookingTimeline.objects.get(pk=pk)
        except BookingTimeline.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        try:
            bookingTimeline = self.get_object(id)
            serializer = BookingTimelineSerializer(bookingTimeline)
            return Response(serializer.data)
        except BookingTimeline.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        bookingTimeline = self.get_object(id)
        serializer = BookingTimelineSerializer(bookingTimeline, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        bookingTimeline = self.get_object(id)
        bookingTimeline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
