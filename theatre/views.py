from rest_framework import generics
from .models import TheatreHall, Play, Genre, Actor, Performance, Reservation, Ticket
from .serializers import (
    TheatreHallSerializer,
    PlaySerializer,
    GenreSerializer,
    ActorSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
)


class TheatreHallListCreateView(generics.ListCreateAPIView):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayListCreateView(generics.ListCreateAPIView):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorListCreateView(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class PerformanceListCreateView(generics.ListCreateAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
