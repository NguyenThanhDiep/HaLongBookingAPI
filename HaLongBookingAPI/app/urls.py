from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    path('hotels/', views.HotelView.as_view()),
    path('hotels/<int:id>/', views.HotelDetailView.as_view()),
    path('rooms/', views.RoomView.as_view()),
    path('rooms/<int:id>/', views.RoomDetailView.as_view()),
    path('bookings/', views.BookingView.as_view()),
    path('bookings/<int:id>/', views.BookingDetailView.as_view()),
    path('admins/', views.AdminView.as_view()),
    path('admins/<int:id>/', views.AdminDetailView.as_view()),
    path('timelines/', views.BookingTimelineView.as_view()),
    path('timelines/<int:id>/', views.BookingTimelineDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
