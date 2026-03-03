# reservation/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer
from django.http import JsonResponse

def eureka_health_check(request):
    """Health check pour Eureka"""
    return JsonResponse({
        "status": "UP",
        "application": "RESERVATION-DJANGO",
        "port": 8000,
        "database": "connected"
    })
@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'OK',
        'service': 'Reservation Microservice',
        'database': 'MongoDB',
        'django_version': '4.2.10'
    })

@api_view(['GET'])
def reservation_list(request):
    """List all reservations"""
    reservations = Reservation.objects.all().order_by('-created_at')
    data = []
    for r in reservations:
        data.append({
            'id': r.id,
            'reservation_number': r.reservation_number,
            'user_id': r.user_id,
            'reservation_type': r.reservation_type,
            'total_price': str(r.total_price),
            'status': r.status,
            'created_at': r.created_at.isoformat()
        })
    return Response(data)

@api_view(['POST'])
def create_reservation(request):
    """Create a new reservation"""
    serializer = ReservationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    reservation = serializer.save(status='PENDING')

    return Response({
        'message': 'Réservation créée avec succès',
        'reservation_number': reservation.reservation_number,
        'id': reservation.id,
        'data': serializer.data
    }, status=status.HTTP_201_CREATED)