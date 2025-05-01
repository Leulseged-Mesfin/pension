from django.urls import path
from .views import (
    RoomTypeCreateListAPIView, 
    RoomTypeRetriveUpdateDeleteAPIView, 
    RoomCreateListAPIView, 
    RoomRetriveUpdateDeleteAPIView, 
    BookingCreateListAPIView, 
    BookingRetriveUpdateDeleteAPIView, 
    GuestCreateListAPIView, 
    GuestRetriveUpdateDeleteAPIView, 
    InvoiceCreateListAPIView, 
    InvoiceRetriveUpdateDeleteAPIView, 
    AuditLogListAPIView
    ) 


urlpatterns = [
    path('room-types/', RoomTypeCreateListAPIView.as_view(), name='room-type-list'),
    path('room-types/<int:pk>', RoomTypeRetriveUpdateDeleteAPIView.as_view(), name='room-type-detail'),
    path('rooms/', RoomCreateListAPIView.as_view(), name='room--list'),
    path('rooms/<int:pk>', RoomRetriveUpdateDeleteAPIView.as_view(), name='room-type-detail'),
    path('guests/', GuestCreateListAPIView.as_view(), name='room-type-list'),
    path('guests/<int:pk>', GuestRetriveUpdateDeleteAPIView.as_view(), name='room-type-detail'),
    path('bookings/', BookingCreateListAPIView.as_view(), name='room-type-list'),
    path('bookings/<int:pk>', BookingRetriveUpdateDeleteAPIView.as_view(), name='room-type-detail'),
    path('invoices/', InvoiceCreateListAPIView.as_view(), name='room-type-list'),
    path('invoices/<int:pk>', InvoiceRetriveUpdateDeleteAPIView.as_view(), name='room-type-detail'),
    path('audit-logs/', AuditLogListAPIView.as_view(), name='audit-log-list'),
]

