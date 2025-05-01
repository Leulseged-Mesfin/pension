from rest_framework import serializers
from .models import RoomType, Room, Guest, Booking, Invoice, AuditLog

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomgetSerializer(serializers.ModelSerializer):
    room_type = serializers.CharField(source='room_type.name', read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingGetSerializer(serializers.ModelSerializer):
    guest = serializers.CharField(source='guest.full_name', read_only=True)
    room = serializers.CharField(source='room.number', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'guest', 'room', 'check_in', 'check_out', 'status', 'created_at']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

