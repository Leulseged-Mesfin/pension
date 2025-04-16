from django.urls import path
from .views import RoomTypeCreateListAPIView, RoomTypeRetriveUpdateDeleteAPIView


urlpatterns = [
    path('room-types/', RoomTypeCreateListAPIView.as_view(), name='room-type-list'),
    path('room-types/<int:pk>/', RoomTypeRetriveUpdateDeleteAPIView.as_view(), name='room-type-detail'),
]

