# reservation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('eureka-health/', views.eureka_health_check, name='eureka-health'),
    path('reservations/', views.reservation_list, name='reservation-list'),
    path('reservations/create', views.create_reservation, name='reservation-create-no-slash'),
    path('reservations/create/', views.create_reservation, name='reservation-create'),
 ]