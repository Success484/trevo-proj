from django.contrib import admin
from main_app.models import Order, TrackingEvent

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("tracking_number", "sender_name", "receiver_name", "payment_status", "created_at")
    search_fields = ("tracking_number", "sender_name", "receiver_name")

@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "location", "timestamp")
    search_fields = ("order__tracking_number", "status", "location")