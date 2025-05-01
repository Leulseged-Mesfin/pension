from django.db import models
from decimal import Decimal

# Create your models here.
class RoomType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)  # e.g., Single, Double, Suite
    description = models.TextField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Occupied", "Occupied"),
        ("Cleaning", "Cleaning"),
        ("Maintenance", "Maintenance"),
    ]

    number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available", null=True, blank=True)
    floor = models.PositiveIntegerField(null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Room {self.number} - {self.room_type.name}"


class Guest(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    id_document = models.CharField(max_length=50)  # Passport or national ID
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class Booking(models.Model):
    STATUS_CHOICES = [
        ("Booked", "Booked"),
        ("Checked In", "Checked In"),
        ("Checked Out", "Checked Out"),
        ("Cancelled", "Cancelled"),
    ]

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Booked")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest.full_name} - Room {self.room.number}"
    
    # Example of how to calculate room_charges
    def calculate_room_charges(booking):
        nights = (booking.check_out - booking.check_in).days
        return booking.room.price_per_night * nights
    
    def change_room_status(self):
        if self.status == "Checked In":
            self.room.status = "Occupied"
        elif self.status == "Checked Out":
            self.room.status = "Available"
        elif self.status == "Cancelled":
            self.room.status = "Available"
        else:
            raise ValueError("Invalid booking status.")
        self.room.save()

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            if self.check_in >= self.check_out:
                raise ValueError("Check-out date must be after check-in date.")
        super().save(*args, **kwargs)


class Invoice(models.Model):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Debit Card", "Debit In"),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    tax = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash", null=True, blank=True)  # e.g., Credit Card, Cash

    def __str__(self):
        return f"Invoice for {self.booking}"
    
    def save(self, *args, **kwargs):
        if self.booking:
            # Calculate room charges
            self.room_charges = self.booking.calculate_room_charges()
            self.tax = round((self.room_charges + self.extra_charges) * Decimal('0.15'), 2)

            self.total_amount = self.room_charges + self.extra_charges + self.tax

        super().save(*args, **kwargs)


class SeasonalRate(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    adjusted_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.room_type.name} from {self.start_date} to {self.end_date}"


class OccupancyReport(models.Model):
    date = models.DateField(unique=True, null=True, blank=True)
    total_rooms = models.PositiveIntegerField(null=True, blank=True)
    rooms_occupied = models.PositiveIntegerField(null=True, blank=True)

    @property
    def occupancy_rate(self):
        if self.total_rooms == 0:
            return 0
        return round((self.rooms_occupied / self.total_rooms) * 100, 2)

    def __str__(self):
        return f"Occupancy on {self.date}"


class PricingRule(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100, null=True, blank=True)  # e.g., "occupancy < 30"
    adjustment = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # e.g., -10.00 for discount
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f"{self.room_type.name} Rule: {self.condition}"


class AuditLog(models.Model):
    user = models.CharField(max_length=100, null=True, blank=True)  # e.g., username or email
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"