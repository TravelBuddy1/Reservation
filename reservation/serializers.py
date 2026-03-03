# reservation/serializers.py
from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reservation_type_display = serializers.CharField(source='get_reservation_type_display', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['id', 'reservation_number', 'created_at', 'updated_at']

class HostReservationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    host_id = serializers.IntegerField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    number_of_guests = serializers.IntegerField(min_value=1, default=1)
    
    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class ActivityReservationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    activity_id = serializers.IntegerField()
    activity_date = serializers.DateTimeField()
    participants = serializers.IntegerField(min_value=1, default=1)