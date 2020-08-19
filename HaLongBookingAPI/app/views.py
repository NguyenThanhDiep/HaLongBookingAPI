from app.models import Hotel, Room
from app.serializers import HotelSerializer, HotelDetailSerializer, RoomSerializer, RoomDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.
class HotelView(APIView):
    def get(self, request, format=None):
        hotels = Hotel.objects.all()
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
            return Room.objects.create(name=model['name'], srcImg=model['srcImg'], price=model['price'], freeServices=model['freeServices'], capacity=model['capacity'], hotel=hotel)
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
