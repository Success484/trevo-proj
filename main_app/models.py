from django.db import models
import random, string

# Create your models here.

def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

class Order(models.Model):
    tracking_number = models.CharField(max_length=12, unique=True, default=generate_tracking_number, editable=False)
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    SERVICE_TYPE = [
        ('sea', 'Sea Delivery'),
        ('land', 'Land Delivery'),
        ('Air', 'Air Delivery')
    ]
    # SHIPMENT DETAILS
    quantity = models.IntegerField()
    weight = models.FloatField(default=0.5)
    service_type = models.CharField(max_length=200, choices=SERVICE_TYPE, default='land')
    goods_description = models.TextField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='pending')
    # DESTINATION DETAILS
    receiver_name = models.CharField(max_length=100)
    receiver_email = models.EmailField(max_length=200)
    receiver_address = models.CharField(max_length=255)
    date_of_delivery = models.CharField(max_length=255)
    # ORIGIN
    sender_name = models.CharField(max_length=100)
    pickup_address = models.CharField(max_length=255)
    sender_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)
    # current_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.sender_name} to {self.receiver_name}"

class TrackingEvent(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_transit", "In Transit"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("failed_attempt", "Failed Attempt"),
        ("returned", "Returned"),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="events")
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    note = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.order.tracking_number} - {self.status} at {self.location}"
