from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    path('hotels/', views.HotelView.as_view()),
    path('hotels/<int:id>/', views.HotelDetailView.as_view()),
    path('rooms/', views.RoomView.as_view()),
    path('rooms/<int:id>/', views.RoomDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
