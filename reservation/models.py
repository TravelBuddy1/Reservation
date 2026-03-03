# reservation/models.py
from django.db import models
from django.utils import timezone
import uuid

class Reservation(models.Model):
    RESERVATION_TYPES = [
        ('HOST', 'Hébergement'),
        ('ACTIVITY', 'Activité'),
        ('COMBO', 'Combiné'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('CANCELLED', 'Annulée'),
        ('COMPLETED', 'Terminée'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    reservation_number = models.CharField(max_length=50, unique=True)
    
    # User info (from User Microservice)
    user_id = models.IntegerField()
    user_email = models.EmailField(max_length=200, blank=True)
    user_name = models.CharField(max_length=200, blank=True)
    
    # Reservation type
    reservation_type = models.CharField(max_length=20, choices=RESERVATION_TYPES)
    
    # For HOST reservations
    host_id = models.IntegerField(null=True, blank=True)
    host_name = models.CharField(max_length=200, blank=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    number_of_guests = models.IntegerField(default=1)
    nights = models.IntegerField(default=0)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # For ACTIVITY reservations
    activity_id = models.IntegerField(null=True, blank=True)
    activity_name = models.CharField(max_length=200, blank=True)
    activity_date = models.DateTimeField(null=True, blank=True)
    participants = models.IntegerField(default=1)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # For COMBO (both)
    items = models.JSONField(default=list, blank=True)
    
    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Feedback tracking
    feedback_given = models.BooleanField(default=False)
    feedback_id = models.IntegerField(null=True, blank=True)
    feedback_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reservations'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['reservation_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.reservation_number} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            import random
            import string
            date_str = timezone.now().strftime('%y%m%d')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.reservation_number = f"RES-{date_str}-{random_str}"
        super().save(*args, **kwargs)