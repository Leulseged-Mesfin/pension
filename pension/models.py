from django.db import models

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
    floor = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Room {self.number} - {self.room_type.name}"



class Guest(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    id_document = models.CharField(max_length=50, null=True, blank=True)  # Passport or national ID
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
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Booked", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest.full_name} - Room {self.room.number}"



class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    tax = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)  # e.g., Credit Card, Cash

    def __str__(self):
        return f"Invoice for {self.booking}"



class SeasonalRate(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    adjusted_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.room_type.name} from {self.start_date} to {self.end_date}"




class OccupancyReport(models.Model):
    date = models.DateField(unique=True, null=True, blank=True)
    total_rooms = models.IntegerField(null=True, blank=True)
    rooms_occupied = models.IntegerField(null=True, blank=True)

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
